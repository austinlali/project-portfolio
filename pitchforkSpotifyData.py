import argparse
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('ggplot')


class PitchforkSpotifyData:

    def __init__(self, args):
        self.args = args
        logging.debug("init PitchforkSpotifyData")

        self._load_spotify()
        self._load_pitchfork()

        if self.args.plotData:
            logging.debug("plots will be generated")
            self.plot_top5()
            self.plot_attributesAndScores()
            self.plot_scatter()

    def _load_spotify(self):
        # read spotify data and group by artist to get the average metric for each music attribute
        self.spot = pd.read_csv(filepath_or_buffer='data/data_by_artist.csv', header='infer')
        self.spot = self.spot.groupby(by=['artists']).mean()
        logging.debug('spotify dataframe created')
        # set both indexes all to lower case to account for differences in artist names
        self.spot.index = self.spot.index.str.lower()

    def _load_pitchfork(self):
        # read pitchfork data and group by artist to get the average review scores
        self.pfork = pd.read_csv(filepath_or_buffer='data/reviews.csv', header='infer')
        logging.debug('pfork dataframe created')

    def _prep_top5(self):
        """Creates a plot based on data on artists in the pitchfork data file"""
        # calculate which artists have the most reviews with a rating greater than 8.0. exclude 'various artists'
        keep8OrMore = self.pfork[self.pfork['score'] >= 8.0]
        logging.debug("keep only albums with a score of 8 or more")
        dropVarious = keep8OrMore[keep8OrMore['artist'] != 'various artists']
        logging.debug("drop various artists for artist plot")
        logging.debug("create dataframe for artist plot")
        cntByArtist = dropVarious.groupby(by=['artist']).count()
        # merge the restructured review data to spotify data and select the top 5 who match
        self.joinTop5 = cntByArtist.join(self.spot, how='inner').nlargest(5, 'reviewid')
        logging.debug('top 5 dataframe created')


    def _prep_scatter(self):
        # join pfork and spotify data into one data from using the artist as the index for scatter plot
        self.pfork = self.pfork.groupby(by=['artist']).mean()
        # set both indexes all to lower case to account for differences in artist names
        self.pfork.index = self.pfork.index.str.lower()
        join = self.pfork.join(self.spot, how='inner')
        join = join.drop(
            columns=['reviewid', 'Unnamed: 0', 'best_new_music', 'pub_weekday', 'pub_day', 'pub_month', 'pub_year',
                     'reviewid.1', 'valence', 'popularity', 'key', 'mode', 'count'])
        logging.debug('new dataframe created with joined data')
        self.scatter = join
        logging.debug('data frame of spotify and pitchfork merged data successfully created')

    def _prep_scoreBuckets(self):
        # create buckets for scores (<6, 6-7, 7-8, 8-9, 9-10)
        self._prep_scatter()
        scoreBuckets = self.scatter
        scoreBuckets['scoreGrps'] = ''
        scoreBuckets.loc[scoreBuckets['score'] <= 6, 'scoreGrps'] = '6 or lower'
        scoreBuckets.loc[(scoreBuckets['score'] > 6) & (scoreBuckets['score'] <= 7), 'scoreGrps'] = '6 to 7'
        scoreBuckets.loc[(scoreBuckets['score'] > 7) & (scoreBuckets['score'] <= 8), 'scoreGrps'] = '7 to 8'
        scoreBuckets.loc[(scoreBuckets['score'] > 8) & (scoreBuckets['score'] <= 9), 'scoreGrps'] = '8 to 9'
        scoreBuckets.loc[(scoreBuckets['score'] > 9) & (scoreBuckets['score'] <= 10), 'scoreGrps'] \
            = '9 to 10'
        self.GroupByBucket = scoreBuckets.groupby(by=['scoreGrps']).mean()
        logging.debug('socre bucket dataframe created')


    def plot_attributesAndScores(self):
        self._prep_scoreBuckets()
        # plot the average music attributes of score groupings
        logging.debug('creating plot')
        df = self.GroupByBucket

        labels = df.index.to_numpy()
        dance = df['danceability'].to_numpy()
        en = df['energy'].to_numpy()
        instr = df['instrumentalness'].to_numpy()
        live = df['liveness'].to_numpy()
        acoustic = df['acousticness'].to_numpy()
        speech = df['speechiness'].to_numpy()

        x = np.arange(len(labels))

        width = 0.10

        fig, ax = plt.subplots()

        rects1 = ax.bar(x - 5 * width / 2, dance, width, label='Danceability')
        rects2 = ax.bar(x - 3 * width / 2, en, width, label='Energy')
        rects3 = ax.bar(x - 1 * width / 2, instr, width, label='Instrumentalness')
        rects4 = ax.bar(x + 1 * width / 2, live, width, label='Liveness')
        rects4 = ax.bar(x + 3 * width / 2, acoustic, width, label='Acousticness')
        rects5 = ax.bar(x + 5 * width / 2, speech, width, label='Speechiness')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Values')
        ax.set_title('Music Attributes by Score Groupings')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(prop={'size': 8})

        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.savefig("pitchforkSpotifyData_combined_attributes_by_score_group.png")
        plt.show()
        logging.debug('showing plot and saving as png to local directory')


    def plot_top5(self):
        self._prep_top5()

        # plot the average music attributes by top 5 artists
        logging.debug('creating plot')
        df = self.joinTop5

        labels = df.index.to_numpy()
        dance = df['danceability'].to_numpy()
        en = df['energy'].to_numpy()
        instr = df['instrumentalness'].to_numpy()
        live = df['liveness'].to_numpy()
        acoustic = df['acousticness'].to_numpy()
        speech = df['speechiness'].to_numpy()

        x = np.arange(len(labels))

        width = 0.10

        fig, ax = plt.subplots()

        rects1 = ax.bar(x - 5 * width / 2, dance, width, label='Danceability')
        rects2 = ax.bar(x - 3 * width / 2, en, width, label='Energy')
        rects3 = ax.bar(x - 1 * width / 2, instr, width, label='Instrumentalness')
        rects4 = ax.bar(x + 1 * width / 2, live, width, label='Liveness')
        rects4 = ax.bar(x + 3 * width / 2, acoustic, width, label='Acousticness')
        rects5 = ax.bar(x + 5 * width / 2, speech, width, label='Speechiness')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Values')
        ax.set_title('Music Attributes by Top 5 Artists')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(prop={'size': 8})

        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.savefig("pitchforkSpotifyData_combined_attributes_of_top_5_reviewed_artists.png")
        plt.show()
        logging.debug('showing plot and saving as png to local directory')


    def plot_scatter(self):
        self._prep_scatter()
        # create a dataframe of the 500 top scored artists
        df = self.scatter.nlargest(500, 'score')

        # create a figure with 4 subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        logging.debug('creating plot')

        # create numpy arrays of the review scores and associated music attribute scores
        scores = df['score'].to_numpy()
        # acoust = df['acousticness'].to_numpy()
        # dance = df['danceability'].to_numpy()
        # en = df['energy'].to_numpy()
        instr = df['instrumentalness'].to_numpy()
        live = df['liveness'].to_numpy()
        loud = df['loudness'].to_numpy()
        speech = df['speechiness'].to_numpy()
        # temp = df['tempo'].to_numpy()
        logging.debug('creating numpy arrays')

        # make 4 scatter plots that plot the score vs. a selected music attribute
        ax1.scatter(scores, live, c="green", label='Liveness')
        ax2.scatter(scores, loud, c="blue", label='Loudness')
        ax3.scatter(scores, speech, c="red", label='Speechiness')
        ax4.scatter(scores, instr, c="purple", label='Instrumentalness')
        logging.debug('creating scatter plots')

        # add legends to each subplot
        ax1.legend(prop={'size': 8})
        ax2.legend(prop={'size': 8})
        ax3.legend(prop={'size': 8})
        ax4.legend(prop={'size': 8})
        logging.debug('creating legends')

        # add a title and axis lables to the overall figure
        fig.suptitle("Music Attribute Ratings for the Top 500 Rated Artists on Pitchfork", fontsize=12)
        fig.text(0.5, 0.04, 'Average Review Score', ha='center', va='center')
        fig.text(0.06, 0.5, 'Music Attribute Value', ha='center', va='center', rotation='vertical')
        logging.debug('adding labels')

        # show and save the visual as a png
        plt.savefig("pitchforkSpotifyData_combined_score_vs_music_attribute.png")
        plt.show()
        logging.debug('showing plot and saving as png to local directory')


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

    parser = argparse.ArgumentParser(description='pitchforkSpotifyData is a module that uses Pitchfork Review and \
                                     Spotify data to plot the musical characteristics of top rated artists.')

    parser.add_argument('-p', '--plot', dest='plotData', action='store_true',
                        help='if flagged, create data plots')

    args = parser.parse_args()
    logging.debug("argParse")

    PitchforkSpotifyData(args)
    logging.debug("complete")


if __name__ == '__main__':
    main()
