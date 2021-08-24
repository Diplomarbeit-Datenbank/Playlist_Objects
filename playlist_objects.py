"""

    This is a file which creates a Playlist canvas which all functions of a Playlist like create, modify and so on

    Note: This file work in cooperation with the Music_Widget.py file from Christof Haidegger
          -> Music_Widget.py had to be in the same folder as this file itself

"""

from tkinter import filedialog
import Ctkinter as Ctk
import tkinter as tk
import Music_Widget  # this is required to start a new Playlist
import shutil
import glob
import sys
import os


__date__ = '17.08.2021'
__completed__ = '24.08.2021'
__work_time__ = 'about 9 Hours'
__author__ = 'Christof Haidegger'
__version__ = '1.0'
__licence__ = 'Common Licence'
__debugging__ = 'Christof Haidegger'


class Playlist_objects:
    """

        -> All Objects for a Playlist with all functions of a nice

    """
    def __init__(self, master) -> None:
        """

        :param master: master where the playlist object should be placed
        """
        self.create_thumbnail_button = None
        self.thumbnail_image_path = None
        self.create_playlist_window = None
        self.name_entry = None
        self.selected_song_list = list()
        self.__PLAYLIST_DIRECTORY__ = 'Playlists/'
        self.__SONG__DIRECTORY__ = 'Songs/'
        self.playlist_object = Ctk.CCanvas(master=master, bg='gray30', size=(500, 300), corners='rounded', max_rad=30)
        self.playlist_object.create_line(2, 65, 500, 65, fill='white')

        info_label = Ctk.CLabel(master=self.playlist_object, bg=self.playlist_object['background'], size=(250, 50),
                                text='Playlists', fg='white', font=('Helvetica', 25), corner='angular')
        info_label.place(x=10, y=10)

        # Run Functions

        self._create_option_buttons()
        self.scroll_canvas = self._create_playlist_scroll_widget()

    def _create_option_buttons(self) -> None:
        """

            -> This function create the two Buttons New Playlist and Delete Playlist

        """
        new_playlist_button = Ctk.CButton(self.playlist_object, bg='gray12', highlight_color='gray8',
                                          pressing_color='black', width=245, height=30, text='New Playlist',
                                          font=('Helvetica', 15), fg='white', rounded_corners='round',
                                          command=self._create_new_playlist)
        new_playlist_button.place(x=3, y=70)

        delete_playlist_button = Ctk.CButton(self.playlist_object, bg='gray12', highlight_color='gray8',
                                             pressing_color='black', width=245, height=30, text='Delete Playlist',
                                             font=('Helvetica', 15), fg='white', rounded_corners='round',
                                             command=self.delete_playlist)
        delete_playlist_button.place(x=250, y=70)

    def _create_playlist_scroll_widget(self) -> Ctk.CCanvas:
        """

        :return: A Ctk.CCanvas with the items on the scrollbar (the scrollbar had only to be placed on the interface)
        """
        background_canvas = Ctk.CCanvas(master=self.playlist_object, bg='gray20', size=(490, 185), corners='rounded',
                                        max_rad=40)
        playlists = self._get_all_playlists()
        if len(playlists) >= 4:
            scroll_width = 168
        else:
            scroll_width = len(playlists) * 42

        playlist_canvas = Ctk.CScrollWidget(master=background_canvas.get_canvas(), width=475, height=scroll_width,
                                            bg=background_canvas['background'])

        for counter, playlist in enumerate(playlists):
            if playlist is not None:
                play_name = playlist.split('\\')[-2]
                number_of_songs = len(self._get_all_songs(playlist + 'song_paths.txt'))
                gif_path = playlist + 'thump.gif'
            else:
                play_name = 'All Songs'
                number_of_songs = len(self._get_all_songs())
                gif_path = 'images/fun.gif'
            if playlist is not None:
                single_playlist_button = Ctk.CButton(master=playlist_canvas.get_master_for_placing_objects(),
                                                     bg='gray15', highlight_color='gray25',
                                                     pressing_color='gray12', width=469, height=40, fg='white',
                                                     rounded_corners='rounded',
                                                     command=lambda play=playlist: Music_Widget.
                                                     MusicPlayerWidget(None).
                                                     start_new_playlist(playlist_path=play + 'song_paths.txt'))
            else:
                single_playlist_button = Ctk.CButton(master=playlist_canvas.get_master_for_placing_objects(),
                                                     bg='gray15', highlight_color='gray25',
                                                     pressing_color='gray12', width=469, height=40, fg='white',
                                                     rounded_corners='rounded',
                                                     command=lambda play=playlist: Music_Widget.
                                                     MusicPlayerWidget(None).
                                                     start_new_playlist(playlist_path=play))

            gif_canvas = Ctk.CCanvas(master=single_playlist_button, bg=single_playlist_button['background'],
                                     size=(34, 34), corners='angular')
            gif_canvas.create_gif(gif_path=gif_path, corner='round', size=(45, 45), pos=(18, 18), transparent=True)
            gif_canvas.place(x=5, y=2)
            single_playlist_button.set_button_atributes(gif_canvas.get_canvas(), gif_canvas.outline)

            info_label = Ctk.TextAnimation(master=single_playlist_button.get_canvas(),
                                           bg=single_playlist_button['background'], size=(150, 35), text=play_name,
                                           font=('Helvetica', 16), fg='white',
                                           label_place=(10, 5), text_space=30)
            info_label.animated_text.place(x=50, y=4)

            single_playlist_button.set_button_atributes(info_label.get_label(), None)
            single_playlist_button.set_button_atributes(info_label.animated_text, None)

            info_label1 = Ctk.CLabel(master=single_playlist_button, bg=single_playlist_button['background'],
                                     size=(245, 34), text='Number of Songs: ' + str(number_of_songs), fg='white',
                                     font=('Helvetica', 16), corner='angular', text_place=(10, 6))
            info_label1.place(x=200, y=3)

            single_playlist_button.set_button_atributes(info_label1.get_canvas(), info_label1.CLabel.outline)

            if play_name != 'All Songs':
                settings_button = Ctk.CButton(master=single_playlist_button, bg=single_playlist_button['background'],
                                              highlight_color=None,
                                              pressing_color=None, width=33, height=33,
                                              rounded_corners='angular',
                                              image=('images/settings.png', 'angular', (16, 16), (35, 35)),
                                              command=lambda name=play_name: self._create_new_playlist(name))
                settings_button.place(x=430, y=4)

                single_playlist_button.set_button_atributes(settings_button.get_canvas(), settings_button.polygon,
                                                            set_command=False)

            single_playlist_button.grid(row=counter, column=0, padx=3, pady=0)

        playlist_canvas.place(x=10, y=10)
        background_canvas.place(x=5, y=110)

        return background_canvas

    def delete_playlist(self):
        """

        : create a tkinter window, where a playlist can be deleted
        """

        def get_all_inputs():
            """

            :return: a list of all indexes which are selected on the list item from tkinter
            """
            selected_list = list()
            selected = song_list_box.curselection()
            for index in selected:
                selected_list.append(index)

            return selected_list

        def confirm_remove_playlist(same):
            """

            :return: delete the playlist
            """

            selected_playlist_names = [item for count, item in
                                       enumerate(
                                           [element for element in same._get_all_playlists() if element is not None])
                                       if count in get_all_inputs()]

            for playlist_name in selected_playlist_names:
                shutil.rmtree(playlist_name)

            playlist_root.destroy()
            same.scroll_canvas = same._create_playlist_scroll_widget()

        def cancel_delete(same):
            """

            :param same: same is eco to self
            """
            playlist_root.destroy()
            same.scroll_canvas = same._create_playlist_scroll_widget()

        self.scroll_canvas.destroy()
        playlist_names = map(lambda item: item.split('\\')[-2],
                             [name for name in self._get_all_playlists() if name is not None])
        playlist_root = tk.Toplevel()
        playlist_root.config(bg='gray20')
        playlist_root.geometry("300x220")
        playlist_root.title('Remove Playlist')
        playlist_root.protocol("WM_DELETE_WINDOW", lambda: cancel_delete(self))

        # create info label:
        info1 = tk.Label(playlist_root, text='Delete Playlists', font=('Helvetica', 15), fg='white',
                         bg=playlist_root['background'])
        info1.place(x=0, y=1)

        # create listbox with songs
        song_list_box = tk.Listbox(playlist_root, selectmode=tk.MULTIPLE, width=68, height=9, bd=-1,
                                   bg='gray20', font=('Helvetica', 10), fg='white')

        song_list_box.place(x=-1, y=35)

        for cnt, playlist in enumerate(playlist_names):
            song_list_box.insert(cnt, ' ' + playlist)

        confirmation_button = tk.Button(playlist_root, text='Confirm', bg='gray25', fg='white', font=('Sans', 10),
                                        command=lambda: confirm_remove_playlist(self))
        confirmation_button.pack(fill='x', side='bottom')
        playlist_root.mainloop()

    def _get_all_playlists(self) -> list:
        """

        :return: a list of all Playlists which are available
        """
        playlist_paths = glob.glob(self.__PLAYLIST_DIRECTORY__ + '*/')
        playlist_paths.insert(0, None)
        return playlist_paths

    def _create_new_playlist(self, name=None) -> None:
        """

        :param name: name of the Playlist (This param is only to take, if the Playlist does already exist and only had
                     to be changed in its properties

        """
        create_playlist_window = tk.Toplevel()
        create_playlist_window.title('Create New Playlist')
        create_playlist_window.config(bg=self.playlist_object['background'])
        create_playlist_window.geometry('400x200')

        self.create_thumbnail_button = Ctk.CButton(master=create_playlist_window, bg='gray12', highlight_color='gray20',
                                                   pressing_color='gray9', width=150, height=150, text='+',
                                                   font=('Helvetica', 80), fg='white', courser="hand2", outline=('', 1),
                                                   rounded_corners='rounded',
                                                   command=lambda: self._add_thumbnail(create_playlist_window),
                                                   max_rad=None)
        self.create_thumbnail_button.place(x=20, y=38)

        info_thumbnail_label = Ctk.CLabel(master=create_playlist_window, bg=create_playlist_window['background'],
                                          size=(150, 30), text='Thumbnail (GIF):', fg='white', font=('Helvetica', 15),
                                          corner='angular', text_place=(5, 2))
        info_thumbnail_label.place(x=5, y=5)
        if name is None:
            info_text = 'Name: '
        else:
            info_text = 'New Name: '
        name_info_label = Ctk.CLabel(master=create_playlist_window, bg=create_playlist_window['background'],
                                     size=(150, 30), text=info_text, fg='white', font=('Helvetica', 16),
                                     corner='angular', text_place=(5, 2))
        name_info_label.place(x=185, y=40)
        if name is None:
            self.name_entry = Ctk.CLabel(master=create_playlist_window, size=(200, 30), text='', fg='black',
                                         font=('Helvetica', 13), corner='round', max_rad=None, outline=('', 0),
                                         anchor='NW', variable_text=True, enter_hit=(True, lambda: self._save_playlist),
                                         text_place=(10, 5), text_width=20)
            self.name_entry.place(x=190, y=75)
        else:
            self.name_entry = Ctk.CLabel(master=create_playlist_window, size=(200, 30), text='', fg='black',
                                         font=('Helvetica', 13), corner='round', max_rad=None, outline=('', 0),
                                         anchor='NW', variable_text=True,
                                         text_place=(10, 5), text_width=20)
            self.name_entry.place(x=190, y=75)

        if name is not None:
            self.name_entry.insert(name)

        add_music_info_label = Ctk.CLabel(master=create_playlist_window, bg=create_playlist_window['background'],
                                          size=(150, 30), text='Add Songs:', fg='white', font=('Helvetica', 16),
                                          corner='angular', text_place=(5, 2))
        add_music_info_label.place(x=185, y=120)

        if name is None:
            args = None
        else:
            args = self.__PLAYLIST_DIRECTORY__ + name + '/song_paths.txt'

        browse_music_button = Ctk.CButton(master=create_playlist_window, bg='white', highlight_color='white',
                                          pressing_color='gray20', width=200, height=30, text='Add Songs',
                                          font=('Helvetica', 13), fg='black', courser="hand2", outline=('', 1),
                                          rounded_corners='round',
                                          command=lambda: self._open_add_delete_song_list(args),
                                          max_rad=None, dash=None)
        browse_music_button.place(x=190, y=155)

        if name is None:
            arg = False
        else:
            arg = True

        create_button = Ctk.CButton(master=create_playlist_window, bg='gray18', highlight_color='gray12',
                                    pressing_color='black', width=60, height=23,
                                    text='Create', font=('Helvetica', 12), fg='white',
                                    command=lambda: self._save_playlist(None, arg, name))
        create_button.place(x=340, y=2)

        self.create_playlist_window = create_playlist_window
        create_playlist_window.mainloop()

    def _save_playlist(self, _, over_write=False, name=None) -> None:
        """

        :param _: this param is a placeholder for the event param of the Ctkinter library
        :param over_write: if this is true, the playlist does already exist and should be exchanged with new params
        :param name: name of the playlist if it does already exist (otherwise None) -> default

        :raises: In line 343 a error when the same gif is in the same folder selected (nobody do this shit!)
        """
        self.scroll_canvas.destroy()

        if self.name_entry.get() == '':
            return
        if over_write is False:
            try:
                os.mkdir(self.__PLAYLIST_DIRECTORY__ + self.name_entry.get() + '/')
            except FileExistsError:
                print('Playlist does already exist')
                return

        if name != self.name_entry.get() and over_write is True:
            os.mkdir(self.__PLAYLIST_DIRECTORY__ + self.name_entry.get() + '/')

        if not self.selected_song_list:
            self.selected_song_list = list(enumerate(self._get_all_songs(self.
                                                                         __PLAYLIST_DIRECTORY__ +
                                                                         name + '/song_paths.txt')))

        song_paths_txt = open(self.__PLAYLIST_DIRECTORY__ + self.name_entry.get() + '/song_paths.txt', 'w')

        for counter, (_, song_path) in enumerate(self.selected_song_list):
            if counter < len(self.selected_song_list) - 1:
                song_paths_txt.write(song_path + '\n')
            else:
                song_paths_txt.write(song_path)

        song_paths_txt.close()
        if self.thumbnail_image_path is not None:
            try:
                shutil.copy2(self.thumbnail_image_path,
                             self.__PLAYLIST_DIRECTORY__ + self.name_entry.get() + '/thump.gif')
            except shutil.SameFileError:
                print('Depp kunsch ja nit in selben gif nomol nehmen des geht ja nitta :|',  file=sys.stderr)

        if name != self.name_entry.get() and over_write is True:
            if self.thumbnail_image_path is None:
                print('Hallo')
                shutil.copy2(self.__PLAYLIST_DIRECTORY__ + name + '/thump.gif',
                             self.__PLAYLIST_DIRECTORY__ + self.name_entry.get() + '/thump.gif')

            shutil.rmtree(self.__PLAYLIST_DIRECTORY__ + name + '/')

        self.create_playlist_window.destroy()

        self.scroll_canvas.destroy()
        self.scroll_canvas = self._create_playlist_scroll_widget()

    def _get_all_songs(self, direct=None) -> list:
        """
        :param direct: directory to search for songs
        :return: a list with the song directories
        """
        if direct is None:
            song_directories = glob.glob(self.__SONG__DIRECTORY__ + '*/')
        else:
            file = open(direct, 'r')
            songs = file.read().split('\n')
            song_directories = [item for item in songs if item != '']

            file.close()

        return song_directories

    def _open_add_delete_song_list(self, playlist_dir=None) -> None:
        """

        :param playlist_dir: if the playlist does already exist playlist dir is the path to the song_paths.txt in the
                             playlist folder

        """
        def get_all_inputs(get):
            """

            :param get: get == self !!!!!
            """
            get.selected_song_list = list()
            selected = song_list_box.curselection()
            for index in selected:
                get.selected_song_list.append((index, song_path_list[index]))

            add_delete_song_list_window.destroy()

        add_delete_song_list_window = tk.Toplevel()
        add_delete_song_list_window.title('Choose Songs')
        add_delete_song_list_window.geometry("400x236")
        add_delete_song_list_window.config(bg='gray20')
        add_delete_song_list_window.resizable(False, False)

        info_label = tk.Label(master=add_delete_song_list_window, text='Songs: ', font=('Helvetica', 15), fg='white',
                              bg='gray20')
        info_label.place(x=3, y=3)

        # create listbox with songs
        song_list_box = tk.Listbox(add_delete_song_list_window, selectmode=tk.MULTIPLE, width=68, height=10, bd=-1,
                                   bg='gray20', font=('Helvetica', 10), fg='white')

        song_list_box.place(x=-1, y=35)
        if playlist_dir is not None:
            selected_songs = self._get_all_songs(playlist_dir)
            indexes = [counter for counter, item in enumerate(self._get_all_songs()) if item in selected_songs]
            self.selected_song_list = list(zip(indexes, selected_songs))

        # insert all songs
        song_path_list = self._get_all_songs()
        for song in song_path_list:
            song_name = '  ' + song.split('\\')[-2]
            song_list_box.insert(tk.END, song_name)

        for value, _ in self.selected_song_list:
            song_list_box.select_set(value)

        # buttons:
        but_cancel = Ctk.CButton(master=add_delete_song_list_window, bg='gray15', highlight_color='gray12',
                                 pressing_color='black', width=200, height=30, text='Cancel', font=('Helvetica', 15),
                                 fg='black', rounded_corners='angular', command=print)
        but_cancel.place(x=-1, y=205)

        but_continue = Ctk.CButton(master=add_delete_song_list_window, bg='gray15', highlight_color='gray12',
                                   pressing_color='black', width=200, height=30, text='Continue',
                                   font=('Helvetica', 15), fg='black', rounded_corners='angular',
                                   command=lambda: get_all_inputs(self))
        but_continue.place(x=199, y=205)

        add_delete_song_list_window.mainloop()

    def _add_thumbnail(self, master):
        """

        :param master: master, where the thumbnail is to place

        """
        file = filedialog.askopenfile(title='Choose a GIF', filetypes=[('GIF', '.gif')])
        self.create_thumbnail_button.destroy()
        gif_canvas = Ctk.CCanvas(master=master, bg=master['background'], size=(150, 150), corners='angular')
        gif_canvas.create_gif(gif_path=file.name, corner='round', size=(149, 149), pos=(76, 76), transparent=True)
        gif_canvas.place(20, 38)
        self.thumbnail_image_path = file.name
        master.lift()


def main():
    """

        -> This is just to test the software itself

    """
    root = tk.Tk()
    root.config(bg='white')
    root.title('download object test')

    download_ob = Playlist_objects(root)
    download_ob.playlist_object.grid(row=0, column=1, padx=15)

    media_player = Music_Widget.MusicPlayerWidget(root)
    media_player.music_player_widget.grid(row=0, column=0)

    root.mainloop()


if __name__ == '__main__':
    main()
