from google.cloud import vision
import argparse
import json
from pprint import pprint

class TextDetect():

    def encrypt(self,letter, key):

        # must be single alphabetic character
        if not letter.isalpha() or len(letter) != 1:
            return letter

        # convert to lowercase
        letter = letter.lower()

        # convert to numerical value 0 - 25
        # a = 0, b = 1, ... z = 25
        value = ord(letter) - 97

        # apply key, number of characters to shift
        value = (value + key) % 26

        # return encrypted letter
        return chr(value + 97)


    def decrypt(self,letter, key):

        # must be single alphabetic character
        if not letter.isalpha() or len(letter) != 1:
            return letter

        # convert to lowercase
        letter = letter.lower()

        # convert to numerical value 0 - 25
        # a = 0, b = 1, ... z = 25
        value = ord(letter) - 97

        # apply key, number of characters to shift
        value = (value - key) % 26

        # return encrypted letter
        return chr(value + 97)


    def caesar_encode(self, message, key):
        # encipher
        ciphertext = ''
        for letter in message:
            ciphertext += self.encrypt(letter, key)

        return ciphertext

    def brute_force(self, texts, key):
        """Brute forces each string using caesar cipher
        Returns a list of decoded messages.
        """

        results={}
        results["key"]= key
        decoded=[]

        for text in texts:
            content = text.description
            plaintext = ''
            for letter in content:
                plaintext += self.decrypt(letter, key)

            decoded.append(plaintext)

        results["decoded"]=decoded
        return results


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
    print("""

 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄       ▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀  ▐░▌   ▐░▌  ▀▀▀▀█░█▀▀▀▀      ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀
     ▐░▌     ▐░▌            ▐░▌ ▐░▌       ▐░▌          ▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌          ▐░▌               ▐░▌
     ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄    ▐░▐░▌        ▐░▌          ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌               ▐░▌
     ▐░▌     ▐░░░░░░░░░░░▌    ▐░▌         ▐░▌          ▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌               ▐░▌
     ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀    ▐░▌░▌        ▐░▌          ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀      ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌               ▐░▌
     ▐░▌     ▐░▌            ▐░▌ ▐░▌       ▐░▌          ▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌          ▐░▌               ▐░▌
     ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄  ▐░▌   ▐░▌      ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌
     ▐░▌     ▐░░░░░░░░░░░▌▐░▌     ▐░▌     ▐░▌          ▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌
      ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀       ▀       ▀            ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀


    """)
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--brute", action="store_true",
                        help="brute force image text")

    parser.add_argument("-c", "--ce", action="store_true",
                        help="encode using Caesar Cipher")

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
    elif args.ce:
        if args.verbose:
            print("Encoding Message using Caesar Cipher")
        key=33
        message = t.caesar_encode("This is a test", key)
        print(message)
        plaintext = ''
        for letter in message:
            plaintext += t.decrypt(letter, key)
        print(plaintext)

    else:
        if args.verbose:
            print("Processing image at uri: "+path+"...")
        results= t.detect_text_uri(path)
        report["text"]=results

    pprint(report, indent=4)


if __name__ == '__main__':
    main()
    # detect_text_uri("https://cdn.shortpixel.ai/client/q_glossy,ret_img,w_1632/https://westartwithgood.co/wp-content/uploads/2018/03/trace-expand.png")
