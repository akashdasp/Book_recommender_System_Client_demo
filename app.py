from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
import folium
popular_df=pickle.load(open("popular.pkl",'rb'))
pt=pickle.load(open('pt.pkl','rb'))
final_book_list=pickle.load(open("final_book_list",'rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
final_ratings_with_age=pickle.load(open('final_ratings_with_age.pkl','rb'))
locations=pickle.load(open("location.pkl",'rb'))



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
        return render_template('recommend.html',data=data,user=user_input)
    else:
        random_popular_df = pd.Series(popular_df['Book-Title'].unique()).sample(4).values
        data_1 = []
        for i in range(len(random_popular_df.tolist())):
            item = []
            title = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Book-Title'][:1].values
            item.extend(title)
            author = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Book-Author'][:1].values
            item.extend(author)
            url = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Image-URL-L'][:1].values
            item.extend(url)
            data_1.append(item)
        return render_template('recommend.html',data=data_1,user=user_input)

@app.route('/trending')
def trending():
    random_popular_df = pd.Series(popular_df['Book-Title'].unique()).sample(4).values
    data = []
    for i in range(len(random_popular_df.tolist())):
        item = []
        title = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Book-Title'][:1].values
        item.extend(title)
        url = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Image-URL-L'][:1].values
        item.extend(url)
        author = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Book-Author'][:1].values
        item.extend(author)
        data.append(item)
    return render_template('trending.html',data=data)
@app.route('/demo')
def demo_ui():
    return render_template('demo_implement.html')
@app.route('/location')
def location():
    m = folium.Map(location=locations[5], zoom_start=4)
    for lat, lng in locations:
        folium.CircleMarker(location=[lat, lng],
                            radius=6,
                            fill=True,
                            color='red',
                            fill_color='red',
                            fill_opacity=0.5).add_to(m)


    map_html=m._repr_html_()
    return render_template('location.html',map_html=map_html)

@app.route('/demo_implimentation', methods = ['POST',"GET"])
def implement():
    user_input=request.form.get("user_input")

    if user_input in final_book_list:
        temp_1 = books[books["Book-Title"] == user_input].head(1)
        book_name = list(temp_1["Book-Title"])
        book_author = list(temp_1["Book-Author"])
        img = list(temp_1['Image-URL-L'])
        index = np.where(pt.index == user_input)[0][0]
        similer_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:4]
        data = []
        for i in similer_items:
            item = []
            temp_df = books[books["Book-Title"] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-L"].values))
            data.append(item)
        return render_template('demo_implement.html',data=data,user=user_input,book_name=book_name,book_author=book_author,img=img)
    else:
        random_popular_df = pd.Series(popular_df['Book-Title'].unique()).sample(3).values
        temp_1 = books[books["Book-Title"] == user_input].head(1)
        book_name = list(temp_1["Book-Title"])
        book_author = list(temp_1["Book-Author"])
        img = list(temp_1['Image-URL-L'])
        data_1 = []
        for i in range(len(random_popular_df.tolist())):
            item = []
            title = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Book-Title'][:1].values
            item.extend(title)
            author = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Book-Author'][:1].values
            item.extend(author)
            url = books.loc[books['Book-Title'] == random_popular_df.tolist()[i], 'Image-URL-L'][:1].values
            item.extend(url)
            data_1.append(item)
        return render_template('demo_implement.html',data=data_1,user=user_input,book_name=book_name,book_author=book_author,img=img)
@app.route('/age')
def age_ui():
    return render_template('age_based_recommend.html')
@app.route('/age_recommendation',methods=['POST'])
def classify_age():
    age=int(request.form.get("user_input"))
    if age <=20:
        age_return="0-20"
    elif age>20 and age<=30:
        age_return="21-30"
    elif age>30 and age<=40:
        age_return="31-40"
    elif age>40 and age<=50:
        age_return="41-50"
    elif age>50 and age<=60:
        age_return="51-60"
    elif age>60 and age<=70:
        age_return="61-70"
    elif age>70 and age<=80:
        age_return="61-70"
    elif age>80 and age<=100:
        age_return="61-70"
    else:
        age_return = "31-40"
    temp_df=final_ratings_with_age[final_ratings_with_age['Age_bins']==age_return].sample(8)
    book_title=list(temp_df["Book-Title"].values)
    book_author=list(temp_df["Book-Author"].values)
    publisher=list(temp_df["Publisher"].values)
    img=list(temp_df["Image-URL-L"].values)


    return render_template('age_based_recommend.html',book_title=book_title,book_author=book_author,publisher=publisher,
                           img=img,age=age)


if __name__=="__main__":
    app.run(debug=True)