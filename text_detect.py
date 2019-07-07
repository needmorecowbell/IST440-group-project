from google.cloud import vision
import argparse
import json
from pprint import pprint
import subprocess
import io

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

    def caesar_decode_bash(self, message, maxKey=50):
        """Caesar decode over bash script"""
        results= subprocess.run(["tools/caesar_decode.sh",message, str(maxKey)], stdout=subprocess.PIPE)
        results= results.stdout.decode("utf-8")
        return results.split("\n")

    def caesar_decode(self, texts, key):
        """Brute forces each string using caesar cipher
        Returns a list of decoded messages.
        """

        results={}
        results["key"]= key
        decoded=[]

        for text in texts:
            if(isinstance(text,str)):
                content = text
            else:
                content=text.description
            plaintext = ''
            for letter in content:
                plaintext += self.decrypt(letter, key)

            decoded.append(plaintext)

        results["decoded"]=decoded
        return results

    def detect_text_local(self, path):
        """Detects text in the file."""
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts
  
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

    parser.add_argument("-d", "--cd", action="store_true",
                        help="decode using Caesar Cipher (max key input expected)")
    parser.add_argument( "--cdb", action="store_true",
                        help="decode using bash Caesar Cipher (max key input expected)")

    
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="verbose mode")

    parser.add_argument("path", help="uri of image to process or text to decode")

    args= parser.parse_args()

    t = TextDetect()
    #Get Path Argument (file url or directory)
    path = args.path

    report= {}

    report["target"]=path

    if args.brute:
        if args.verbose:
            print("Processing image at uri: "+path+"...")

        results= t.detect_text_uri(path)
        report["text"]= []
        for result in results:
            report["text"].append(result.description)

        if args.verbose:
            print("Brute forcing image text...")

        resultsCaesar= t.caesar_decode(results, 33)
        report["caesar"]=resultsCaesar
        report["caesarbash"]= []
        report["rot13"]= []
        for result in results:
            print(result.description)
            report["caesarbash"].append(t.caesar_decode_bash(result.description))
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
    elif args.cdb:
        if args.verbose:
            print("Decoding Message using Caesar Cipher")
        report["caesarbash"] = t.caesar_decode_bash(args.path)
    elif args.cd:
        if args.verbose:
            print("Decoding Message using Caesar Cipher")
        report["caesar"] = t.caesar_decode([args.path],33)
              
    else:
        if args.verbose:
            print("Processing image at uri: "+path+"...")
        results= t.detect_text_uri(path)
        report["text"]=results

    pprint(report, indent=4)


if __name__ == '__main__':
    main()
    # detect_text_uri("https://cdn.shortpixel.ai/client/q_glossy,ret_img,w_1632/https://westartwithgood.co/wp-content/uploads/2018/03/trace-expand.png")
