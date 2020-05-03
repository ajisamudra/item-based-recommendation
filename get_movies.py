from imdb import IMDb
import pandas as pd
import datetime as dt


def pull_movies(mv_list):
    movies = []
    for i in range(len(mv_list)):
        movies.append( IMDb().get_movie(mv_list[i]) )
    return movies

def handle_persons(persons):
    str = ""
    i = 0
    for person in persons:
        str += person['name']
        i += 1
        if i < len(persons):
            str += ", "
    return str

def handle_companies(companies):
    str = ""
    i = 0
    for company in companies:
        str += company['name']
        i += 1
        if i < len(companies):
            str += ", "
    return str

def handle_list(lis):
    str = ""
    i = 0
    for item in lis:
        str += item
        i += 1
        if i < len(lis):
            str += ", "
    return str

def extract_data(movie, features):
    data = []
    for f in features:
        if (f == 'genre') or (f == 'runtimes') or (f == 'plot'):
            information = handle_list(movie[f])
        elif isinstance(movie[f], list):
            information = handle_persons(movie[f])
        else:
            information = (movie[f])
        data.append(information)
    return data

def concat_new_data(df, new_df):
    res_df = pd.DataFrame()
    res_df = pd.concat([df, new_df], sort= False)
    return res_df

def create_dataframe(movie_list, features):
    res_df = pd.DataFrame(columns= ['movieID'] + features)
    for i in range(len(movie_list)):
        print(dt.datetime.now())
        print('Getting data movieID: {}'.format(movie_list[i]))
        m =  IMDb().get_movie(movie_list[i])
        new_data = []
        new_data = extract_data(m, features)
        new_row = pd.DataFrame([[movie_list[i]] + new_data], columns= ['movieID'] + features)
        res_df = concat_new_data(res_df, new_row)
        res_df = res_df.reset_index(drop= True)
        print(dt.datetime.now())
        print('Writing data movieID: {} to csv'.format(movie_list[i]))
        res_df.to_csv('top250imdb.csv', index=False)
    return res_df

def get_top250_movielist():
    movie_list = []
    top250 = IMDb().get_top250_movies()
    for i in range(len(top250)):
        movie_list.append( top250[i].movieID )

    return movie_list

if __name__ == '__main__':
    ia = IMDb()
    # movie_list = ['4154796', '0133093', '4154796' ]
    movie_list = get_top250_movielist()
    features = ['title', 'rating', 'votes', 'year', 'writer', 'cast', 'genre', 'kind', 'cover url',
    'director', 'production companies', 'runtimes', 'top 250 rank', 'plot'] 
    print('Starting getting movies information')
    df = create_dataframe(movie_list, features)
    print('Complete')
    print(df)
    # mv = ia.get_movie('4154796') # Avenger
    # top250 = ia.get_top250_movies()
