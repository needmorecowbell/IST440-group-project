from google.cloud import vision
import argparse
import json
from pprint import pprint

class TextDetect():
    def brute_force(self, texts):
        for text in texts:
            content = text.description
            print(content)


    def detect_text_uri(self,uri):
        """Detects text in the file located in Google Cloud Storage or on the Web.
        """
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts

        # for text in texts:
        #     print('\n"{}"'.format(text.description))
        #
        #     vertices = (['({},{})'.format(vertex.x, vertex.y)
        #                 for vertex in text.bounding_poly.vertices])

            #print('bounds: {}'.format(','.join(vertices)))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--brute", action="store_true",
                        help="brute force image text")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="verbose mode")

    parser.add_argument("path", help="uri of image to process")

    args= parser.parse_args()
    t = TextDetect()
    #Get Path Argument (file url or directory)
    path = args.path

    report= {}

    report["uri"]=path

    if args.brute:
        if args.verbose:
            print("Processing image at uri: "+path+"...")

        results= t.detect_text_uri(path)
        report["text"]= results

        if args.verbose:
            print("Brute forcing image text...")

        results= t.brute_force(results)
        report["brute_force"]=results

    else:
        if args.verbose:
            print("Processing image at uri: "+path+"...")
        results= t.detect_text_uri(path)
        report["text"]=results

    pprint(report, indent=4)


if __name__ == '__main__':
    main()
    # detect_text_uri("https://cdn.shortpixel.ai/client/q_glossy,ret_img,w_1632/https://westartwithgood.co/wp-content/uploads/2018/03/trace-expand.png")
