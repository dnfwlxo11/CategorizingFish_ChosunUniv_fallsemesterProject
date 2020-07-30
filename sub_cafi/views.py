from django.shortcuts import render
from .forms import UploadForm
from django.shortcuts import redirect


# Create your views here.

def index(request):
    return render(request, 'sub_cafi/index.html', {})

def image_list(request):
    if request.method == 'POST':
        return render(request, 'sub_cafi/list.html', {})
    elif request.method == 'GET':
        return redirect('upload_image')

def upload_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        result_cafi = ''

        if form.is_valid():
            form.save()
            # -*- coding: utf-8 -*-

            """Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

            import numpy as np
            import tensorflow as tf

            imagePath = 'media\\' + str(request.FILES['pic'])  # 추론을 진행할 이미지 경로
            modelFullPath = 'cafi_model\\output_graph.pb'  # 읽어들일 graph 파일 경로
            labelsFullPath = 'cafi_model\\output_labels.txt'  # 읽어들일 labels 파일 경로

            def create_graph():
                """저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
                # 저장된(saved) graph_def.pb로부터 graph를 생성한다.
                with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
                    graph_def = tf.GraphDef()
                    graph_def.ParseFromString(f.read())
                    _ = tf.import_graph_def(graph_def, name='')

            def run_inference_on_image():
                answer = None

                if not tf.gfile.Exists(imagePath):
                    tf.logging.fatal('File does not exist %s', imagePath)
                    return answer

                image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

                # 저장된(saved) GraphDef 파일로부터 graph를 생성한다.
                create_graph()

                with tf.Session() as sess:

                    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                    predictions = sess.run(softmax_tensor,
                                           {'DecodeJpeg/contents:0': image_data})
                    predictions = np.squeeze(predictions)

                    top_k = predictions.argsort()[-5:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
                    f = open(labelsFullPath, 'rb')
                    lines = f.readlines()
                    labels = [str(w).replace("\n", "") for w in lines]
                    for node_id in top_k:
                        human_string = labels[node_id]
                        human_string = human_string.replace('b\'', '')
                        human_string = human_string.replace('\\n\'', '')
                        score = predictions[node_id]
                        print('%s (score = %.5f)' % (human_string, score))
                        labels[node_id] = human_string

                    answer = labels[top_k[0]]
                    return answer, predictions[top_k[0]]
                    
            result_name, result_score = run_inference_on_image()
            result_cafi = str(str(result_score * 100)[:5] + '%확률로 ' + result_name + '로 추정됩니다')
            print(str(result_score * 100)[:5] + '%확률로 ' + result_name + '로 추정됩니다')

        print(result_cafi)
        cafi_data = {'data':result_cafi, 'img_name':str(request.FILES['pic'])}
        return render(request, 'sub_cafi/list.html', {'data':cafi_data})
    else:
        form = UploadForm()

    return render(request, 'sub_cafi/upload.html', {
        'form': form
    })