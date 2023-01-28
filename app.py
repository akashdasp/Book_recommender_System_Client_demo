from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
popular_df=pickle.load(open("popular.pkl",'rb'))
pt=pickle.load(open('pt.pkl','rb'))
final_book_list=pickle.load(open("final_book_list",'rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))


app=Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           total_rating=list(popular_df['num_ratings'].values),
                           avg_rating=list(popular_df['avg_ratings'].values))

@app.route('/recommend')
def recommed_ui():
    return render_template('recommend.html')
@app.route('/recommend_books',methods = ['POST',"GET"])
def recommend():
    user_input=request.form.get("user_input")
    if user_input in final_book_list:
        index = np.where(pt.index == user_input)[0][0]
        similer_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:5]
        data = []
        for i in similer_items:
            item = []
            temp_df = books[books["Book-Title"] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-L"].values))
            data.append(item)
        return render_template('recommend.html',data=data)
    else:
        random_popular_df = pd.Series(popular_df['Book-Title'].unique()).sample(10).values

@app.route('/trending')
def trending():
    return render_template('trending.html')

if __name__=="__main__":
    app.run(debug=True)