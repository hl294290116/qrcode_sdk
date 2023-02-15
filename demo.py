import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import glob
import argparse
import os
import pyzxing 

import os.path as osp


def visualize(image, text, rect=None, corners=None, type="默认"):
    if rect is not None:
        (x, y, w, h) = rect   # 提取二维码的位置,然后用边框标识出来在视频中
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    elif corners is not None:
        cv2.polylines(image, np.max(np.array([corners], dtype=np.int32), 0), True, (0, 0, 255), 4)
        x, y = corners[0][0]
    else:
        raise Exception("No position information.")

    # print(text)
    img_PIL = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) 
    font_size = image.shape[1] // 20 
    # font = ImageFont.truetype('MSYHL.TTC', font_size)      # 参数（字体，大小）  
    font = ImageFont.truetype('Symbol.ttf', font_size)      # 参数（字体，大小）  

    fillColor = (255, 0, 0)      # 字体颜色（rgb)  
    position = (x, max(0, y-50))      # 文字输出位置  
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, text[:20], font=font, fill=fillColor)
    return cv2.cvtColor(np.array(img_PIL), cv2.COLOR_RGB2BGR)


def run_qrcode(input_path, output_path):
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    for barcode in barcodes:
        text = barcode.data.decode("utf-8")
        if True:
            result_path = input_path.replace(".png", ".txt")
            with open(result_path) as f:
                data = f.read()
            if text != data:
                print(f"文件: {input_path} 二维码类别： {barcode.type} 内容： {text}, benchmark: {data}")             
        image = visualize(image, text, rect=barcode.rect, type=barcode.type)
        # print(f"二维码类别： {barcode.type} 内容： {text}")
    cv2.imwrite(output_path, image)


def run_single(input_path, output_path, debug=False):
    # print("## zbar")
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    if len(barcodes):
        for barcode in barcodes:
            text = barcode.data.decode("utf-8")
            image = visualize(image, text, barcode.rect, barcode.type)
            print(f"条码类别： {barcode.type} 内容： {text}")
        cv2.imwrite(output_path, image)
        if not debug:
            return

    # print("## OpenCV")
    image = cv2.imread(input_path)
    bardet = cv2.barcode_BarcodeDetector()
    ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(image)
    if ok:
        image = visualize(image, decoded_info[0], corners=corners, type=decoded_type)
        cv2.imwrite(output_path, image)
        if not debug:
            return

    # print("## zxing")
    reader = pyzxing.BarCodeReader()
    # results = reader.decode(input_path)
    # 支持传入图片的向量
    # 需要额外安装opencv，pip install opencv-python
    results = reader.decode(input_path)
    for res in results:
        print(res)
        if "parsed" not in res:
            continue
        text = res["parsed"].decode()
        points = [[(int(x), int(y)) for x, y in res["points"]]]
        image = visualize(image, text, corners=points, type=decoded_type)
        cv2.imwrite(output_path, image)

    # print("## WeChat")
    detector = cv2.wechat_qrcode_WeChatQRCode("detect.prototxt", "detect.caffemodel", "sr.prototxt", "sr.caffemodel")
    image = cv2.imread(input_path)
    results, points = detector.detectAndDecode(image)
    if len(results):
        for text, pts in zip(results, points):
            print(text, pts)
            image = visualize(image, text, corners=[pts], type=decoded_type)

        cv2.imwrite(output_path, image)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Bar/QR Code Recognition")

    parser.add_argument('--image_path', type=str, required=False, help='path to input image')
    parser.add_argument('--vis_path', type=str, required=False, help='path to output image')

    args = parser.parse_args()
    
    if args.image_path:
        run_single(args.image_path, args.vis_path, debug=False)
    else:
        # 二维码
        img_dir = './dataset'
        output_dir = './output/qrcode'
        if not osp.isdir(output_dir):
            os.makedirs(output_dir)
        for img in glob.glob(f'{img_dir}/*.png'):
            output_path = f'{output_dir}/{osp.basename(img)}'
            run_qrcode(img, output_path)

        # 条形码
        # img_dir = '../imgs/barcode'
        # output_dir = '../output/barcode'
        # if not osp.isdir(output_dir):
        #     os.makedirs(output_dir)
        # for img in glob.glob(f'{img_dir}/*'):
        #     output_path = f'{output_dir}/{osp.basename(img)}'
        #     run_barcode(img, output_path)