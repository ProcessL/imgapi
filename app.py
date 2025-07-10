from flask import Flask, request, jsonify
import os
import api.changebg as changebg
import api.changecloth as changecloth
import api.expand as expand
import api.fix as fix
import api.koutu as koutu
import config

app = Flask(__name__)


@app.route('/change_bg', methods=['POST'])
def run_changebg():
    base_image_url = request.json.get('base_image_url')
    ref_image_url = request.json.get('ref_image_url')
    ref_prompt = request.json.get('ref_prompt', "")  # 可选参数，默认为空字符串
    n = request.json.get('n', 1)  # 可选参数，默认为1

    if not base_image_url or not ref_image_url:
        return jsonify({"error": "Missing image URLs"}), 400

    try:
        task_id = changebg.start_image_synthesis(base_image_url, ref_image_url, ref_prompt, n)
        result = changebg.poll_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/change_cloth', methods=['POST'])
def run_changecloth():
    top_garment_url = request.json.get('top_garment_url')
    bottom_garment_url = request.json.get('bottom_garment_url')
    person_image_url = request.json.get('person_image_url')
    if not all([top_garment_url, bottom_garment_url, person_image_url]):
        return jsonify({"error": "Missing garment or person image URLs"}), 400

    try:
        task_id = changecloth.start_image_synthesis(top_garment_url, bottom_garment_url, person_image_url)
        result = changecloth.poll_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/expand', methods=['POST'])
def run_expand():
    base_image_url = request.json.get('base_image_url')
    top_scale = request.json.get('top_scale', 1.5)
    bottom_scale = request.json.get('bottom_scale', 1.5)
    left_scale = request.json.get('left_scale', 1.5)
    right_scale = request.json.get('right_scale', 1.5)
    prompt = request.json.get('prompt', '按照原来图片背景来操作扩展')

    if not base_image_url:
        return jsonify({"error": "Missing base image URL"}), 400

    try:
        task_id = expand.start_image_synthesis(base_image_url, top_scale, bottom_scale, left_scale, right_scale, prompt)
        result = expand.poll_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fix', methods=['POST'])
def run_fix():
    base_image_url = request.json.get('base_image_url')
    prompt = request.json.get('prompt', '图像超分。')

    if not base_image_url:
        return jsonify({"error": "Missing base image URL"}), 400

    try:
        task_id = fix.start_image_synthesis(base_image_url, prompt)
        result = fix.poll_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/remove_bg', methods=['POST'])
def run_koutu():
    image_url = request.json.get('image_url')
    if not image_url:
        return jsonify({"error": "Missing image URL"}), 400

    try:
        result = koutu.perform_image_segmentation(image_url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(host=config.SERVER_HOST, port=config.SERVER_PORT, debug=config.DEBUG_MODE)