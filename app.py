from flask import Flask, render_template, request, flash, url_for, redirect
import pandas as pd
from zipfile import ZipFile
import urllib
from zipfile import ZipFile
from urllib.request import urlretrieve
from os import mkdir

app = Flask(__name__)
app.secret_key = 'mykey'

inputFile = "./dropBoxFile.zip"
outputDir = "dropbox"


@app.route('/')
def index():

    return render_template('home.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        url = request.form['urldata']

        df3, new_filename = urlwrap(url)

        df3.to_csv(r'{}.csv'.format(new_filename), index=False, header=True)

        # print(url)
        # return 'Hello this is send {} and {}'.format(url, new_filename)
    flash(('{}.csv file has been generated for the data at url:{} ').format(
        new_filename, url))
    return redirect(url_for('index'))


def urlwrap(url):

    urlretrieve(url, inputFile)

    with ZipFile(inputFile) as zipObj:
        zipObj.extractall(outputDir)

        new_filename = url[42:49]  # Reads link and outputs ID
        # print(new_filename)

    with ZipFile('dropBoxFile.zip') as zipObj:
        # Get list of files names in zip
        custID = zipObj.namelist()
        # Iterate over the list of file names in given list & print them
        # for pics in listOfiles:
        # print(pics)

    df1 = pd.DataFrame(custID, columns=['custID'])
    df1['custID'] = df1['custID'].str[:4]
    df1['custID'] = df1['custID'].astype(int)

    df2 = pd.read_csv('id status.csv')
    df3 = df1.merge(df2, on='custID', how='left')

    return df3, new_filename


if __name__ == "__main__":
    app.run(debug=True)
