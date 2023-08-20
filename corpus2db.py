# import the required libraries
import argparse
import mysql.connector as msql
from mysql.connector import Error
import pandas as pd
import re
import spacy
import nltk
from nltk.tokenize import word_tokenize

# Load the language model to sentencize
nlp = spacy.load('fr_core_news_sm')

# Custom function with nlp.pipes to sentencize
def sentencize(nlp, texts):
    docs = list(nlp.pipe(texts, batch_size=128)) 
    return [list(doc.sents) for doc in docs]

def generate_corpus_index(corpus_name):
    # Convert to lowercase and keep only alphanumeric characters
    cleaned_name = re.sub(r'[^a-zA-Z0-9]', '', corpus_name.lower())
    # Ensure length is up to 15 characters, pad with '0' if needed
    return cleaned_name[:15].ljust(15, '0')

def generate_sub_corpus_index(corpus_index, sub_corpus_name):
    # Convert sub-corpus name to alphanumeric and pad with '0'
    cleaned_sub_corpus_name = re.sub(r'[^a-zA-Z0-9]', '', sub_corpus_name)[:15].ljust(15, '0')
    return f"{corpus_index}_{cleaned_sub_corpus_name}"

def generate_turn_index(sub_corpus_index, turn_number):
    # The turn index is constructed by concatenating the sub-corpus index and the turn number,
    return f"{sub_corpus_index}_{str(turn_number)}"

def generate_speaker_index(sub_corpus_index, spk_name):
    # Convert speaker name to alphanumeric
    try : 
        cleaned_spk_name = re.sub(r'[^a-zA-Z0-9]', '', spk_name)
        # Combine the corpus index and sub-corpus index, and spk name with an underscore to form the speaker index
        speaker_index = f"{sub_corpus_index}_{cleaned_spk_name}"
    except : 
        speaker_index = ''
    # Return the generated speaker index
    return speaker_index

def create_index(df, corpus_name):
    """a function to create all indexes to be implemented in the database"""
    generated_indices = initialize_indices_set()

    #vérification dans la base de donénes à faire
    df['index_corpus']=generate_corpus_index(corpus_name)
    df['index_sub_corpus'] = df.apply(lambda row : generate_sub_corpus_index(row['index_corpus'], row['sub_corpus']), axis=1)
    
    df['nb_index_enregistrement'] = df['index_sub_corpus'].ne(df['index_sub_corpus'].shift()).cumsum()
    df['numero_tour'] = df.groupby('nb_index_enregistrement').cumcount() + 1
    df['index_turn_index'] = df.apply(lambda row : generate_turn_index(row['index_sub_corpus'], row['numero_tour']), axis=1)
    # Additional check to ensure turn indices are unique
    df['index_turn_index'] = df['index_turn_index'].apply(lambda idx: unique_index(idx, generated_indices))
    df['index_spk']= df.apply(lambda row : generate_sub_corpus_index(row['index_sub_corpus'], row['name_speaker']), axis=1)
    return df

def initialize_indices_set():
    return set()

def unique_index(index, generated_indices):
    """
    Ensures generated indices are unique
    """
    if index in generated_indices:
        new_index = f"{index}_dup"
        while new_index in generated_indices:
            new_index += "_dup"
        index = new_index
    generated_indices.add(index)
    return index

def get_MD(list_):
    """a function to get the list of MD"""
    tokens = list(enumerate(list_))
    list_md = ['car','bref','comme','donc','enfin','ensuite','après','puis','puisque','soudain','mais', 'ben']
    index_tokens = [(ind,tok) for ind, tok in tokens if tok.text.lower() in list_md]
    return index_tokens


def tokenize(x):
    if isinstance(x, str):
        tokens= list(enumerate(word_tokenize(x, language='french')))
        list_md = ['car','bref','comme','donc','enfin','ensuite','après','puis','puisque','soudain','mais', 'ben']
        index_tokens = [(ind,tok) for ind, tok in tokens if tok in list_md]
        return index_tokens
    else:
        return []

def create_token_index(tokens, index_tour):
    index_tokens = [str(index_tour)+'_'+str(ind) for ind, tok in tokens]
    return index_tokens


def keep_words(string):
    res = re.sub(r'[^\w\s]', '', string)
    string = string.replace(' ', '')
    return res

def formate2db2(df, name_corpus):
    """This function goes from the original df to the ones corresponding in the tables of the db"""
     #create_new_index
    df.dropna(subset=['text_utterance'], inplace=True) #delete rows with empty text column
    if df['type_corpus'].tolist()[0]=='ecrit':
        type_ = df['type_corpus'].tolist()[0]
        df['doc_sents'] = sentencize(nlp, df['text_utterance'].fillna('')) #sentencize the text
        df = df.explode('doc_sents') #make it 1 row = 1 utterance
        df['text_utterance'] = df['doc_sents'].apply(lambda x: x.text)#ne garder que le texte pour chaque phrase
        df = df.fillna('') #fill the NAN values 
        df = create_index(df, name_corpus) #create the index
        #for the demo version, check if the tokens are dm and extract their position
        df['MD']=df['doc_sents'].apply(lambda x: get_MD(x))
    else:
        type_ = df['type_corpus'].tolist()[0]
        df = df.fillna('') #fill the NAN values
        df = create_index(df, name_corpus) #create the index
        #for the demo version, check if the tokens are dm and extract their position
        df['MD']=df['text_utterance'].apply(lambda x: tokenize(x))
    
    #table corpus
    table_corpus = df[['index_corpus','publisher_corpus', 'author_corpus','type_corpus', 'description_corpus']]
    table_corpus = table_corpus.groupby('index_corpus').agg({
    'publisher_corpus': 'first',
    'author_corpus':'first',
    'type_corpus': 'first', 
    'description_corpus':'first'
    }).reset_index()
    print('table corpus : ok')

    
    #table sub-corpus
    table_enregistrement = df[['index_sub_corpus','index_corpus', 'link_sub_corpus','date_sub_corpus','description_sub_corpus','author_sub_corpus','type_sub_corpus','right_sub_corpus','duration_sub_corpus','acoustic_quality_sub_corpus', 'place_sub_corpus']]#'path_xml',
    table_enregistrement = table_enregistrement.groupby('index_sub_corpus').agg({
    'index_corpus': 'first',
    'link_sub_corpus': 'first',
    'date_sub_corpus': 'first',
    'description_sub_corpus' : 'first',
    'author_sub_corpus' : 'first',
    'type_sub_corpus':'first',
    'right_sub_corpus': 'first',
    'duration_sub_corpus': 'first',
    'acoustic_quality_sub_corpus': 'first',
    'place_sub_corpus': 'first'
    }).reset_index()
    print('table table_enregistrement : ok')
    
#   table utterance
    table_tour = df[['index_turn_index', 'index_sub_corpus', 'text_utterance', 'start_utterance', 'end_utterance']]
    table_tour = table_tour.groupby('index_turn_index').agg({
    'index_sub_corpus': 'first',
    'text_utterance' : 'first',
    'start_utterance':'first',
    'end_utterance' : 'first'
    }).reset_index()
    print('table table_tour : ok')

    #table spk
    table_locuteurs = df[['index_spk','name_speaker', 'age_speaker', 'gender_speaker', 'profession_speaker', 'birth_place_speaker', 'education_speaker', 'french_status_speaker', 'notes_speaker']]
    table_locuteurs = table_locuteurs.groupby('index_spk').agg({
    'name_speaker': 'first',
    'age_speaker': 'first',
    'gender_speaker': 'first',
    'profession_speaker': 'first',
    'birth_place_speaker': 'first',
    'education_speaker': 'first',
    'french_status_speaker': 'first',
    'notes_speaker': 'first'
    }).reset_index()
    print('table table_loc: ok')
    
    #table spk_utt
    table_spk_utt = df[['index_turn_index', 'index_spk']]
    table_spk_utt = table_spk_utt.explode('index_spk')
    print('table spk_utt: ok')
    
    #table dm
    d = {'id_md': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], 'forme': ['car','bref','comme','donc','enfin','ensuite','après','puis','puisque','soudain','mais', 'ben']}
    table_md = pd.DataFrame(d)
    print('table table_md: ok')
    
    #table utt_dm
    table_tour_md = df[['index_turn_index', 'MD']]
    table_tour_md = table_tour_md.explode('MD')
    table_tour_md = table_tour_md.dropna(axis='rows')
    table_tour_md['position'] = table_tour_md['MD'].apply(lambda x : x[0])
    table_tour_md['form'] = table_tour_md['MD'].apply(lambda x : x[1])
    table_tour_md['MD']= table_tour_md['form'].apply(lambda x : map_string_to_integer(x, type_))
    table_tour_md = table_tour_md.explode('MD')

    return table_corpus, table_enregistrement, table_tour, table_locuteurs, table_tour_md, table_spk_utt, table_md


def map_string_to_integer(input_string, type_):
    string_to_int_mapping = {
        'car': '1',
        'bref': '2',
        'comme': '3',
        'donc': '4',
        'enfin': '5',
        'ensuite': '6',
        'après': '7',
        'puis': '8',
        'puisque': '9',
        'soudain': '10',
        'mais': '11',
        'ben': '12'
    }
    if type_ == 'écrit':
        if isinstance(input_string.text, str):
            # Handle single string input
            return string_to_int_mapping.get(input_string.text.lower(), "Not found")
        elif isinstance(input_string, list):
            # Handle list of strings input
            int_list = [string_to_int_mapping.get(string.text.lower(), "Not found") for string in input_string]
            return int_list
        else:
            return "Invalid input"
    else:
        if isinstance(input_string, str):
            # Handle single string input
            return string_to_int_mapping.get(input_string.lower(), "Not found")
        elif isinstance(input_string, list):
            # Handle list of strings input
            print(len(input_string))
            int_list = [string_to_int_mapping.get(string.lower(), "Not found") for string in input_string]
            return int_list
        else:
            return "Invalid input"



def pop_corpus(table):
    """populate the corpus table
    make sure to replace your corpus table columns name"""
    try:
        conn = msql.connect(host='localhost',
                            database='codim_db', user='root',
                            password='')
        if conn.is_connected():
            cursor = conn.cursor()

            for i, row in table.iterrows():
                sql =  "INSERT INTO corpus (id_corpus, publisher_corpus, author_corpus, type_corpus, description_corpus) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(sql, (row['index_corpus'], row['publisher_corpus'], row['author_corpus'], row['type_corpus'], row['description_corpus']))
                print("Record inserted into tour")
            conn.commit()
            print("Data insertion completed.")
    except Error as e:
        print("Table Corpus : Error while connecting to MySQL", e) 
        return False



def pop_database(table_corpus, table_enregistrement, table_tour, table_locuteurs, table_tour_md, table_spk_utt):
    pop_corpus(table_corpus)
    pop_enregistrement(table_enregistrement.fillna(''))
    pop_locuteurs(table_locuteurs)
    pop_tour(table_tour)
    pop_tour_md(table_tour_md)
    pop_spk_utt(table_spk_utt) 
    return True


def pop_enregistrement(table):
    try:
        conn = msql.connect(host='localhost',
                            database='codim_db', user='root',
                            password='')
        if conn.is_connected():
            cursor = conn.cursor()           
            for i, row in table.iterrows():
                sql = "INSERT INTO sub_corpus (id_sub_corpus, id_corpus, link_sub_corpus, date_sub_corpus, description_sub_corpus, author_sub_corpus, type_sub_corpus, `right_sub_corpus`, duration_sub_corpus, acoustic_quality_sub_corpus, place_sub_corpus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (row['index_sub_corpus'], row['index_corpus'], row['link_sub_corpus'], row['date_sub_corpus'], row['description_sub_corpus'], row['author_sub_corpus'],row['type_sub_corpus'],row['right_sub_corpus'],row['duration_sub_corpus'],row['acoustic_quality_sub_corpus'],row['place_sub_corpus']))
                print("Record inserted into tour")
            conn.commit()
            print("Data insertion completed.")
    except Error as e:
        print("Table enregistrement : Error while connecting to MySQL", e) 
        return False


def pop_locuteurs(table):
    table.replace('', None, inplace=True)  # Replace empty strings with None in the DataFrame
    try:
        conn = msql.connect(host='localhost',
                            database='codim_db', user='root',
                            password='')
        if conn.is_connected():
            cursor = conn.cursor()                     
            for i, row in table.iterrows():
                sql = "INSERT INTO speaker (id_speaker, name_speaker, age_speaker, gender_speaker, profession_speaker, birth_place_speaker, education_speaker, french_status_speaker, notes_speaker) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (row['index_spk'], row['name_speaker'], row['age_speaker'], row['gender_speaker'], row['profession_speaker'], row['birth_place_speaker'], row['education_speaker'], row['french_status_speaker'], row['notes_speaker']))
                print("Record inserted into tour")
            conn.commit()
            print("Data insertion completed.")
    except Error as e:
        print("Table locuteurs : Error while connecting to MySQL", e) 
        return False

def pop_tour(table):
    try:
        conn = msql.connect(host='localhost',
                            database='codim_db', user='root',
                            password='')
        if conn.is_connected():
            cursor = conn.cursor()        
            for i, row in table.iterrows():
                sql = "INSERT INTO utterance (id_utterance, id_sub_corpus, text_utterance, start_utterance, end_utterance) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (row['index_turn_index'], row['index_sub_corpus'], row['text_utterance'], row['start_utterance'],row['end_utterance']))
                #print("Record inserted into tour")
            conn.commit()
            #print("Data insertion completed.")
    except Error as e:
        print("Table Tour : Error while connecting to MySQL", e) 
        return False

def clean_diacritics(text):
    if isinstance(text, str):
        text = re.sub(' \+', '', text)
        text = re.sub('///', '', text)
        text = re.sub('=', '', text)
        text = re.sub('^x$', '', text)
        text = re.sub('^m$', 'hum', text)
        text = re.sub('\/([^,]*),[^\/]*\/', r'\1', text)
        text = re.sub(' [^\s]*- ',' ', text)
        text = re.sub('\*rires\*','', text)
        text = re.sub('\*\*\*([^\*]*)\*\*\*', '\1', text)
        text = re.sub('\*\*\*','', text)
        text = re.sub('\*','', text)
        text = re.sub('>','', text)
        text = re.sub('<','', text)
        text = re.sub('###','', text)
        text = re.sub('&','', text)
        text = re.sub('\$\$\$','', text)
        text = re.sub('^X$','', text)
        text = re.sub('\[([^\]]*)]',r'\1', text)
        text = re.sub('\s+#\s?\d([^#]*)#',r'\1',text)
        text = re.sub(':::','', text)
        text = re.sub(':','', text)
        text = re.sub('^X$','',text)
        text = re.sub(r'\sX$','',text)
        text = re.sub(r'^X','',text)
        text = re.sub('/','', text)
        text = re.sub('//','', text)
        text = re.sub('\\\\','', text)
        text = re.sub('^spk\d*','', text)
        text = re.sub('\([^\)]*\)', '', text)
        text = re.sub('[A-Za-z0-9_À-ÿ]*- ','',text)
        text = re.sub('(\w\') (\w)',r'\1\2', text)
        #text = re.sub('([^?]*?)','', text)
        text = re.sub(r'\\','', text)
        text = re.sub(r'/', '', text)
        text = text.replace('  ', ' ')
        text = text.replace('\.h ', '')
        text = text.replace('-~', '')
        text = text.replace('°', '')
        text = text.replace(r'_', '')
        text = text.replace('', '')
        text = text.replace('\` ', '\'')
        text = text.replace('\` ', '\'')
        text = text.replace('à®','î')
        text = text.replace('+', '')
        text = text.replace('\"','')
        text = text.replace('¤','')
        text = text.replace('\x80','')
        text = text.replace('bah','ben')
        text = text.replace('nan','non')
        text = text.replace('Bah','Ben')
        text = text.replace('Nan','Non')
        text = text.replace(' mm ',' hum ')
        text = text.replace('mm ','hum ')
        text = text.replace(' mm',' hum')
        text = text.replace(' hm ',' hum ')
        text = text.replace('xx','')
        text = text.replace('xxxx','')
        text = text.replace('xxx','')
        text = text.replace(' mh',' hum')
        text = text.replace(' mh ',' hum ')
        text = text.replace('mh','hum')
        text = text.replace('XX','')
        text = text.replace(' X ', ' ')
        text = text.replace('NNAAMMEE', '')
        text = text.replace('j` ', 'je ')
        text = text.replace('d` ', 'de ')
        text = text.replace('f`ra', 'fera') #pour clapi)
        text = text.replace('p`t-ête','peut-être')#idem
        text = text.replace('`fin', 'enfin')
        text = text.replace("[", "")
        text = text.replace(']','')
        text = text.strip()
    else:
        print(text)
    return text

def pop_md(table):
    try:
        conn = msql.connect(host='localhost',
                            database='codim_db', user='root',
                            password='')
        if conn.is_connected():
            cursor = conn.cursor()
            for i, row in table.iterrows():
                sql = "INSERT INTO dm (id_dm, form_dm) VALUES (%s, %s)"
                cursor.execute(sql, (row['id_md'], row['forme']))          

            # Commit the changes
            conn.commit()
            print("Data insertion completed.")
    except Error as e:
        print("Table md : Error while connecting to MySQL", e)
        return False

def pop_tour_md(table):
    try:
        conn = msql.connect(host='localhost',
                            database='codim_db', user='root',
                            password='')
        if conn.is_connected():
            cursor = conn.cursor()
            for i, row in table.iterrows():
                sql = "INSERT INTO dm_utterance (id_dm, id_utterance, position) VALUES (%s, %s, %s)"
                cursor.execute(sql, (row['MD'], row['index_turn_index'], row['position']))          

            # Commit the changes
            conn.commit()
            print("Data insertion completed.")
    except Error as e:
        print("Table tour_md : Error while connecting to MySQL", e)
        return False


def pop_spk_utt(table):
    try:
        conn = msql.connect(host='localhost',
                            database='codim_db', user='root',
                            password='')
        if conn.is_connected():
            cursor = conn.cursor()
            for i, row in table.iterrows():
                sql = "INSERT INTO speaker_utterance (id_speaker, id_utterance) VALUES (%s, %s)"
                cursor.execute(sql, (row['index_spk'], row['index_turn_index']))          

            # Commit the changes
            conn.commit()
            print("Data insertion completed.")
    except Error as e:
        print("Table tour_md : Error while connecting to MySQL", e)
        return False

def main(input_path, name_corpus):
    # import the corpus file, process it and insert it into the database
    ok = pd.read_csv(input_path, sep='\t', encoding='utf8')

    # For the demo version
    #ok['name'] = ok['name'].apply(lambda x: re.sub('^20', '', x))
    if ok['type_corpus'].tolist()[0]=='ecrit':
        ok = ok[:10]
    else:
        ok['row_num'] = ok['sub_corpus'].rank(method='dense').sub(1).astype(float)
        ok = ok[ok['row_num'] < 10]
        ok.drop('row_num', axis=1, inplace=True)

    table_corpus, table_enregistrement, table_tour, table_locuteurs, table_tour_md, table_spk_utt, table_md = formate2db2(ok, name_corpus)
    print("Here are the tables to be inserted in the database")
    print(table_corpus)
    print(table_enregistrement)
    print(table_tour)
    print(table_locuteurs)
    print(table_tour_md)
    print(table_spk_utt)
    user_input = input("Are you ok with the tables ? (Type 'T' to confirm and insert them into database, else type anything)")
    if user_input.upper() == "T":
        pop_database(table_corpus, table_enregistrement, table_tour, table_locuteurs, table_tour_md, table_spk_utt)
    else:
        print("Operation canceled.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process input CSV file and populate database.")
    parser.add_argument("input_path", help="Path to the input CSV file")
    parser.add_argument("corpus_name", help="Name of the corpus")
    args = parser.parse_args()

    main(args.input_path, args.corpus_name)