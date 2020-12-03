import argparse
import csv
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.style.use('ggplot')


class SpotifyDataGenres:

    def __init__(self, args):
        self.args = args
        logging.debug("init SpotifyData")

        self._load_data()

        if self.args.plotData == True:
            logging.debug("plots will be generated")
            self.plot_data()    

    
    def _load_data(self):
        logging.debug("reading file by artist")
        read_file = pd.read_csv(filepath_or_buffer='data/data_w_genres.csv')
        
        
        logging.debug("creating initial data frame from raw file")
        df = pd.DataFrame(read_file)
        
        
        # clean data, remove empty genres, erroneous artists, and unneccessary columns
        logging.debug("cleaning data")
        df = df[df.genres != '[]']
        df = df[df.popularity != 0]
        df = df.drop(columns=['duration_ms','valence', 'popularity', 'key', 'mode', 'count'])

        # only take the main genre and omit subgenres
        df['genres'] = df['genres'].apply(lambda x: x.split(',')[0].strip(" []'\""))
        logging.debug("data cleaned")
        
                
        # create a data frame with the average values by genre
        af = df.groupby(by=['genres']).mean()
        logging.debug("creating data frame of averages by genre")
    
        # create another which stores the count of each genre, and remove all columns but 'artists'
        bf = df.groupby(by=['genres']).count()
        bf = bf.drop(columns=['acousticness','danceability','energy','instrumentalness','liveness','loudness','speechiness','tempo'])       
        logging.debug("creating data from of counts by genre")
        
        
        # join both data frames using 'genres' as the key, this will be used for plotting
        cf = af.join(bf, on=['genres'])
        logging.debug("counts and averages successfully joined")
    
    
        # allow for viewing all columns and rows if data is displayed
        pd.set_option('max_columns', None)
        pd.set_option("max_rows", None)
        
        self.data = cf
        logging.debug("data by genre successfully generated and added to self.data")        
        
        
        
        # now we will perform a similar set of operations while using the yearly data
        
        
        # read the yearly data
        read_file = pd.read_csv(filepath_or_buffer='data/data_by_year.csv')
        logging.debug("reading yearly data")
        
        df = pd.DataFrame(read_file)
        logging.debug("creating data frame")
        
        # remove unneccessary columns
        df = df.drop(columns=['duration_ms','valence', 'popularity', 'key', 'mode'])
        logging.debug("cleaning data")


        self.data_by_year = df
        logging.debug("data by year successfully generated and added to self.data_by_year")
        
        
    def list_vars(self):
        logging.debug("listing columns due to -l command line argument")
        for col in self.data:
            print(col)
        
        
            
    def plot_data(self):
        
        #### PLOT TOP GENRES BY NUMBER OF ARTISTS ####

        df = self.data.nlargest(10,'artists')    
        logging.debug("create data frame of top 10 genres by number of artists")
        

        # create a subplot and build a numpy array for the artist counts, genre labels, and y positions on the graph
        fig, ax = plt.subplots()
        artists = df['artists'].to_numpy()
        genres = df.index.to_numpy()
        y_pos = np.arange(len(genres))
        
        logging.debug("building bar chart")        
        
        # create a horizontal bar graph
        ax.barh(y_pos, artists)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(genres)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Total Artists')
        ax.set_title('Top Genres in Spotify by Number of Artists')
        
        
        
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        
        
        plt.show()
        plt.savefig("spotifyData_top_10_genres_by_number_of_artists.png")
        logging.debug("display plot and save as png")
        
        
        
        
        #### PLOT AVERAGE MUSIC METRICS BY TOP GENRES ####
        
        df = self.data.nlargest(5,'artists')
        logging.debug("creating a data frame of top 5 genres by artist count")


        # create the labels and values for each series on the line graph
        labels = df.index.to_numpy()
        dance = df['danceability'].to_numpy()
        en = df['energy'].to_numpy()
        instr = df['instrumentalness'].to_numpy()
        live = df['liveness'].to_numpy()
        acoustic = df['acousticness'].to_numpy()
        speech = df['speechiness'].to_numpy()
        x = np.arange(len(labels))
        logging.debug("all labels and series successfully created")
        
        # width for each bar
        width = 0.10
        
        logging.debug("building bar chart")
        
        # create subplot and add each series as its own set of bars on the graph
        fig, ax = plt.subplots()
        rects1 = ax.bar(x-5*width/2, dance, width, label='Danceability')
        rects2 = ax.bar(x-3*width/2, en, width, label='Energy')
        rects3 = ax.bar(x-1*width/2, instr, width, label='Instrumentalness')
        rects4 = ax.bar(x+1*width/2, live, width, label='Liveness')
        rects4 = ax.bar(x+3*width/2, acoustic, width, label='Acousticness')
        rects5 = ax.bar(x+5*width/2, speech, width, label='Speechiness')
        
        
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Values')
        ax.set_title('Music Attributes by Genre')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(prop={'size': 8})
        
        
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        
        plt.show()
        plt.savefig("spotifyData_music_attributes_of_top_genres.png")
        logging.debug("display plot and save as png")


        
        #### PLOT MUSIC METRIC VALUES BY YEAR OVER LAST 70 YEARS ####
        
        df = self.data_by_year.nlargest(70,'year')
        logging.debug("creating a data frame of the last 70 years worth of data")

        
        
        logging.debug("building line graph")


        # create a subplot and then plot 6 of the music attributes
        
        fig, ax = plt.subplots()
        
        ax.plot(df['year'], df['danceability'], marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=1, label='Danceability')
        ax.plot(df['year'], df['energy'], marker='o', markerfacecolor='blue', markersize=5, color='skyblue', linewidth=1, label='Energy')
        ax.plot(df['year'], df['instrumentalness'], marker='o', markerfacecolor='purple', markersize=5, color='skyblue', linewidth=1, label='Instrumentalness')
        ax.plot(df['year'], df['liveness'], marker='o', markerfacecolor='orange', markersize=5, color='skyblue', linewidth=1, label='Liveness')
        ax.plot(df['year'], df['acousticness'], marker='o', markerfacecolor='yellow', markersize=5, color='skyblue', linewidth=1, label='Acousticness')
        ax.plot(df['year'], df['speechiness'], marker='o', markerfacecolor='green', markersize=5, color='skyblue', linewidth=1, label='Speechiness')
        
        ax.set_ylabel('Values')
        ax.set_title('Music Attributes Over the Years')
        ax.legend(prop={'size': 8})
        
        
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        
        
        plt.show()
        plt.savefig("spotifyData_music_attributes_by_year.png")
        logging.debug("display plot and save as png")
        
        
        
        
def main():
    
    # initialize the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # set debug messages to go to a file
    fh = logging.FileHandler(filename='spotifyData.log', mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    # set debug info to show on the command line
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    parser = argparse.ArgumentParser(description='This parser takes the arguments for the spotifyData module')

    
    parser.add_argument('-p', '--plot', dest='plotData', action='store_true',
                        help='if flagged, create data plots')
    
    
    args = parser.parse_args()
    logging.debug("argParse")

    SpotifyDataGenres(args)
    logging.debug("complete")


if __name__ == '__main__':
    main()