import time
import requests
from typing import List
from multiprocessing import Process

from kafka import KafkaProducer

from chamcong_io.api.producer import ResponseConfig, DataConfig, Camera
from chamcong_io.api.common import Kafka as KafkaIo
from app.core.config import REGISTRY_API
from app.entity.camera import VideoStream


def get_config() -> List[DataConfig]:
    try:
        response = requests.get(REGISTRY_API, timeout=10)
        if response.status_code == 200:
            response_config = response.json()
            config = ResponseConfig(status=response_config["status"], message=response_config["message"], data=response_config["data"])
            return config.data
        else:
            raise Exception(f"request registry failed, status:{response.status_code}")
    except Exception as e:
        raise Exception(f"{e}")    


def run():
    try:
        config = get_config()
        processess = []
        for data in config:
            camera = data.camera
            producer = data.producer
            process = Process(target=produce, args=(camera, producer))
            processess.append(process)
        # start process
        for process in processess:
            process.daemon=True
            process.start()
        # join process
        for process in processess:
            process.join()
    except Exception as e:
        print(e)
        

def produce(camera: Camera, kafka_producer: KafkaIo):
    print(camera)
    print(kafka_producer)
    
    # producer = KafkaProducer(bootstrap_server=kafka_producer.brokers)
    
    # read video
    camera_resource = int(camera.resource) if camera.resource.isnumeric() else camera.resource
    video_stream = VideoStream(camera_resource).start()
    
    while True:
            frame = vs.read()
            if frame is not None:
                frame = cv2.resize(frame, (1280, 720))
                rs, encode_frame = cv2.imencode('.jpg', frame, encode_param)
                print(f"camera: {camera.id}")
                # # produce capture image, may be attach timestamp to message
                # key = MessageKey(camera_id=str(camera_id))
                # p = kafka_producer.send(topic_name, value=encode_frame, key=key.to_string())
                # p.get()
                # display_message = f"camera: {key.get_camera_id()} - Topic: {topic_name} Time: {datetime.fromtimestamp(time.time())} Fps: {round(1/(time.time()-start))}"
                # print(display_message)
    