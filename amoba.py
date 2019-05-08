import numpy as np
import bqplot as bq
from scipy.signal import convolve2d


class gomoku():
    '''
    A simple playable Gomoku board class
    '''

    def __init__(self):
        '''
        Initialization of a Gomoku game with an
        empty board and a random starting party
        '''

        # this holds the information of
        # the current game status
        # 0 means empty place
        # 1 is red
        # 2 is blue
        self.table = np.zeros((15, 15), dtype=int)
        # this holds the history
        self.history = []

        # the visualization of the table is generated by bqplot
        sc_x = bq.LinearScale(max=15.5, min=-1.5)
        sc_y = bq.LinearScale(max=15.5, min=-1.5)
        props = dict(x=[], y=[], scales={'x': sc_x, 'y': sc_y},
                     default_size=500)

        scatt1 = bq.Scatter(colors=['red'], **props)
        scatt2 = bq.Scatter(colors=['blue'], **props)
        winline = bq.Lines(colors=['lightgreen'], stroke_width=5, **props)

        axprops = dict(tick_values=np.arange(16)-0.5,
                       grid_color='black',
                       tick_style={'font-size': 0})
        ax_x = bq.Axis(scale=sc_x, **axprops)
        ax_y = bq.Axis(scale=sc_y, orientation='vertical', **axprops)
        fig = bq.Figure(marks=[scatt1, scatt2, winline], axes=[ax_x, ax_y])
        fig.max_aspect_ratio = 1.0
        fig.min_aspect_ratio = 1.0
        fig.layout.height = '600px'
        self.fig = fig

        # the starting player is randomly selected
        self.who_is_next = np.random.randint(1, 3)
        who = ['red ', 'blue '][self.who_is_next-1]
        self.fig.title = 'Next player is ' + who
        # initially noone is winning
        self.win_string = False

    def check_win(self):
        '''Method for checking if we have a winner.'''
        win_string = False
        # Check if it is a tie
        zx, zy = np.where(self.table == 0)
        if len(zx) == 0:
            self.who_is_next = 4
            self.fig.title = 'It is a TIE!'
            self.win_string = 0, 0, 0, 0
            return win_string

        # kernels
        rw = np.zeros((5, 5), dtype=int)  # row kernel
        rw[2, :] = 1
        co = np.zeros((5, 5), dtype=int)  # culomn kernel
        co[:, 2] = 1
        di = np.zeros((5, 5),  dtype=int)  # diagonal kernel
        di[range(5), range(5)] = 1
        pd = np.rot90(di)              # skew diagonal kernel
        # player tables
        A1 = np.where(self.table == 1, np.ones_like(self.table), np.zeros_like(self.table))
        A2 = np.where(self.table == 2, np.ones_like(self.table), np.zeros_like(self.table))
        # check
        for i, Ai in enumerate([A1, A2]):
            for j, k in enumerate([co, rw, di, pd]):
                check = convolve2d(np.flipud(Ai), k, mode='same')
                xi, yi = np.where(check == 5)
                if xi.size > 0:
                    # if found update figure and return
                    win_string = i+1, xi[0], yi[0], j
                    self.win_string = win_string
                    winner = ['RED ', 'BLUE '][win_string[0]-1]
                    self.fig.title = 'We have a winner: ' + winner
                    orip = [[1, 0], [0, 1], [1, 1], [1, -1]]
                    px, py = orip[j]
                    self.fig.marks[-1].x = yi[0]+py*np.linspace(-2.5, 2.5, 10)
                    self.fig.marks[-1].y = xi[0]+px*np.linspace(-2.5, 2.5, 10)
                    return win_string
        return win_string

    def update_table(self, pos, player, update_figure=True):
        '''
        Based on a new position and player update the game.
        '''

        try:

            is_empty = self.table[pos[0], pos[1]] == 0
            am_i_next = self.who_is_next == player
            game_still_on = player in [1, 2]

            if is_empty*am_i_next*game_still_on:
                self.table[pos[0], pos[1]] = player
                self.history.append([pos,player])
                self.who_is_next = list({1, 2}.difference({player}))[0]
                if update_figure:
                    where1 = np.where(np.flipud(self.table) == 1)
                    where2 = np.where(np.flipud(self.table) == 2)
                    self.fig.marks[0].y, self.fig.marks[0].x = where1
                    self.fig.marks[1].y, self.fig.marks[1].x = where2
                    who = ['red ', 'blue'][self.who_is_next-1]
                    self.fig.title = 'Next player is ' + who
                return True
            else:
                return False
        except Exception as ex:
            print(ex)
            return False

    def reset_table(self):
        '''
        Method to reset game.
        '''

        # noone is winning at the start
        self.win_string = False
        # get a random starting player
        self.who_is_next = np.random.randint(1, 3)
        # reset table data and figure
        self.table = np.zeros((15, 15), dtype=int)
        self.history = []
        for m in self.fig.marks:
            m.x, m.y = [], []

        who = ['red ', 'blue'][self.who_is_next-1]
        self.fig.title = 'Next player is ' + who

    def suggest_random_step(self):
        '''
        Method for suggesting a brainless next step.
        '''

        zx, zy = np.where(self.table == 0)
        if len(zx) == 0:
            self.who_is_next = 4
            self.fig.title = 'It is a TIE!'
        i = np.random.randint(len(zx))
        return [zx[i], zy[i]]
