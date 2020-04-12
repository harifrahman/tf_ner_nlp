from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from serve import prediction_func
import numpy

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    status = 0
    return render_template("index.html", status=status)

@app.route("/api", methods=["POST"])
def submit():
    status = 1
    input_data = request.form['text']
    output_data = prediction_func(input_data)
    splitted_data = []      #untuk data (word + tag)
    split_words = []        #untk word yg sdh di split
    split_tags = []         #untk tags yg sdh di split
    desc = []               #untk desc sesuai tags yg d append
    
    ext_jln = []
    ext_no  = []
    ext_bgn = []
    ext_kel = []
    ext_kec = []
    ext_kab = []
    ext_prov = []
    ext_kpos = []

    print(output_data['tags'][0])

    wordList = input_data.split()
    print(wordList)
    labelList = output_data["tags"]
    for a in range(len(wordList)):
        # mystr = str(wordList[a]) + " <==> " + str(labelList[0][a])
        b_tag = str(labelList[0][a])
        tag = b_tag.replace("b'", "")
        tag = tag.replace("'", "")
        split_words.append(wordList[a])
        # print(tag)
        split_tags.append(tag)


        # conditional statement to classified entities
        if tag == "B-JLN" or tag == "I-JLN":
            ext_jln.append(wordList[a])
            desc.append("Nama Jalan")
        elif tag == "B-NO" or tag == "I-NO":
            ext_no.append(wordList[a])
            desc.append("Nomor")
        elif tag == "B-BGN" or tag == "I-BGN":
            ext_bgn.append(wordList[a])
            desc.append("Bangunan")
        elif tag == "B-KEL" or tag == "I-KEL":
            ext_kel.append(wordList[a])
            desc.append("Desa / Kelurahan")
        elif tag == "B-KEC" or tag == "I-KEC":
            ext_kec.append(wordList[a])
            desc.append("Kecamatan")
        elif tag == "B-KAB" or tag == "I-KAB":
            ext_kab.append(wordList[a])
            desc.append("Kabupaten / Kota")
        elif tag == "B-PROV" or tag == "I-PROV":
            ext_prov.append(wordList[a])
            desc.append("Provinsi")
        elif tag == "B-KPOS" or tag == "I-KPOS":
            ext_kpos.append(wordList[a])
            desc.append("Kodepos")
    #convert they to str to pass 
    s_jln = " ".join(ext_jln)
    s_no  = " ".join(ext_no)
    s_bgn = " ".join(ext_bgn)
    s_kel = " ".join(ext_kel)
    s_kec = " ".join(ext_kec)
    s_kab = " ".join(ext_kab)
    s_prov = " ".join(ext_prov)
    s_kpos = " ".join(ext_kpos)
    data = {"jln":s_jln, "no":s_no, "bgn":s_bgn, "kel":s_kel, "kec":s_kec, "kab":s_kab, "prov":s_prov, "kpos":s_kpos}
    # splitted_data.append(mystr)
    # extraction = [ext_jln, ext_no, ext_bgn, ext_kel, ext_kec, ext_kab, ext_prov, ext_kpos]
    return render_template("index.html", word=input_data, split_words=split_words, split_tags=split_tags, 
        data=data, desc=desc, status=status)





# @app.route("/")
# def index():
#     return render_template("simple_client.html")

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)