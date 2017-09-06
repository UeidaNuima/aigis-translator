from . import api
from flask import request, jsonify
from ..models import File
from mongoengine import Q
from bson import objectid
import json


def retrieve_tree(file_node_current_id=None, depth=0):
    file_tree = []
    if file_node_current_id:
        file_nodes = File.objects(Q(path__size=depth) & Q(path=objectid.ObjectId(file_node_current_id))).only('id', 'name', 'file_type', 'data', 'time_stamp').all()
    else:
        file_nodes = File.objects(Q(path__size=depth)).only('id', 'name', 'file_type', 'data', 'time_stamp').all()
    if file_nodes:
        for file_node in file_nodes:
            leaf = {
                'name': file_node.name,
                'type': file_node.file_type,
                'time_stamp': file_node.time_stamp,
                'id': str(file_node.id),
            }
            if file_node.file_type == 'aar':
                pass
                # leaf['children'] = retrieve_tree(file_node.id, depth + 1)
            elif file_node.file_type == 'atb' or file_node.file_type == 'txt':
                count_sum = len(file_node.data)
                count_translated = 0
                for data_row in file_node.data:
                    if data_row.translation:
                        count_translated += 1
                leaf['count_translated'] = count_translated
                leaf['count_sum'] = count_sum
                leaf['percentage_translated'] = count_translated / count_sum
            file_tree.append(leaf)
    return file_tree


def retrieve_dict(file_node_current, depth=0):
    leaf = {
        'name': file_node_current.name,
        'type': file_node_current.file_type,
    }
    if file_node_current.file_type == 'atb':
        data = {}
        for field in file_node_current.data:
            if field.translation:
                data[field.origin] = field.translation
    elif file_node_current.file_type == 'txt':
        data = {
            'origin': file_node_current.data[0].origin,
            'translation': file_node_current.data[0].translation,
        }
    else:
        # aar
        data = []
        file_nodes = File.objects(Q(path__size=depth + 1) & Q(path=file_node_current.id)).all()
        for file_node in file_nodes:
            data.append(retrieve_dict(file_node, depth + 1))
    leaf['data'] = data
    return leaf


@api.route('/file_list')
def file_list():
    depth = int(request.args.get('level')) if request.args.get('level') else 0
    file_id = request.args.get('id') or None
    file_tree = retrieve_tree(file_node_current_id=file_id, depth=depth)
    return jsonify(file_tree)


@api.route('/file_raw', methods=['GET', 'PUT'])
def file_raw():
    fid = request.args.get('id')
    file_node = File.objects(id=fid).first()

    if not file_node:
        return jsonify({'message': 'File not found.'}), 404

    if request.method == 'GET':
        file_node_parsed = {
            'name': file_node.name,
            'type': file_node.file_type,
            'data': []
        }
        for data in file_node.data:
            file_node_parsed['data'].append({
                'origin': data.origin,
                'translation': data.translation,
                'translator_name': data.translator_name,
                'translator_ip': data.translator_ip,
            })
        return jsonify(file_node_parsed)
    elif request.method == 'PUT':
        try:
            translator_ip = request.remote_addr
            request_data = json.loads(request.get_data())
            translator_name = request_data.get('translator_name')
            index = request_data.get('index')
            translation = request_data.get('translation')
            if file_node.file_type == 'txt':
                translation = translation.replace('\r\n', '\n')
                translation = translation.replace('\n', '\r\n')

            translation_data = file_node.data[index]
            translation_data['translation'] = translation if translation else None
            translation_data['translator_ip'] = translator_ip if translation else None
            translation_data['translator_name'] = translator_name if translation else None

            file_node.save()
            return jsonify({'message': 'OK'})
        except Exception as e:
            return jsonify({'message': str(e)}), 500


@api.route('/file')
def file():
    file_name = request.args.get('file_name')
    file_node = File.objects(name=file_name).first()
    if not file_node:
        return jsonify({'message': 'File not found.'}), 404
    return jsonify(retrieve_dict(file_node))

