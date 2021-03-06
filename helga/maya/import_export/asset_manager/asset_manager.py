

"""
asset_manager
==========================================

GUI to export Alembics from Maya. Building atop of our asset based pipeline.

It takes care of:

#. Cameras
#. Characters
#. Props


-----------------------

Idea list:

#. Queue/Threadpool for alembic export
#. Feed closures to Queue
#. Export chars, props and cameras
#. Use descriptor protocol
#. Take care of preroll for chars in code.

-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""




#Add tool root path
#------------------------------------------------------------------

#import
import sys
import os

#tool_root_path
tool_root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(tool_root_path)





#Import
#------------------------------------------------------------------
#python
import functools
import logging
import subprocess
import time
import shutil
import webbrowser
import yaml
import hashlib
import string
import random
#PySide
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools
import shiboken
import pysideuic




#Import variable
do_reload = True

#helga

#global_variables
from helga.general.setup.global_variables import global_variables
if(do_reload):reload(global_variables)

#global_functions
from helga.general.setup.global_functions import global_functions
if(do_reload):reload(global_functions)

#doc_link
from helga.general.setup.doc_link import doc_link
if(do_reload): reload(doc_link)


#asset_manager

#lib

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)

#asset_manager_logging_handler
from lib import asset_manager_logging_handler
if(do_reload):reload(asset_manager_logging_handler)

#asset_manager_functionality
from lib import asset_manager_functionality
if(do_reload):reload(asset_manager_functionality)

#asset_manager_threads_functionality
from lib import asset_manager_threads_functionality
if(do_reload):reload(asset_manager_threads_functionality)

#asset_manager_alembic_functionality
from lib import asset_manager_alembic_functionality
if(do_reload):reload(asset_manager_alembic_functionality)

#asset_manager_checks
from lib import asset_manager_checks
if(do_reload):reload(asset_manager_checks)

#asset_manager_menu
from lib import asset_manager_menu
if(do_reload):reload(asset_manager_menu)

#lib.gui

#asset_manager_button
from lib.gui import asset_manager_button
if(do_reload):reload(asset_manager_button)

#asset_manager_stylesheet_widget
from lib.gui import asset_manager_stylesheet_widget
if(do_reload):reload(asset_manager_stylesheet_widget)

#asset_manager_stylesheets
from lib.gui import asset_manager_stylesheets
if(do_reload):reload(asset_manager_stylesheets)

#asset_manager_slider_action
from lib.gui import asset_manager_slider_action
if(do_reload):reload(asset_manager_slider_action)

#asset_manager_doublespinbox_action
from lib.gui import asset_manager_doublespinbox_action
if(do_reload):reload(asset_manager_doublespinbox_action)

#asset_manager_doublespinbox_checkable_action
from lib.gui import asset_manager_doublespinbox_checkable_action
if(do_reload):reload(asset_manager_doublespinbox_checkable_action)

#asset_manager_line_edit_checkable_action
from lib.gui import asset_manager_line_edit_checkable_action
if(do_reload):reload(asset_manager_line_edit_checkable_action)

#asset_manager_pre_export_dialog
from lib.gui import asset_manager_pre_export_dialog
if(do_reload):reload(asset_manager_pre_export_dialog)

#asset_manager_dock_widget
from lib.gui import asset_manager_dock_widget
if(do_reload):reload(asset_manager_dock_widget)

#lib.mvc

#shot_metadata_model
from lib.mvc import shot_metadata_model
if(do_reload):reload(shot_metadata_model)

#shot_metadata_view
from lib.mvc import shot_metadata_view
if(do_reload):reload(shot_metadata_view)

#shot_metadata_item_delegate
from lib.mvc import shot_metadata_item_delegate
if(do_reload):reload(shot_metadata_item_delegate)

#shot_metadata_context_menu
from lib.mvc import shot_metadata_context_menu
if(do_reload):reload(shot_metadata_context_menu)


#prop_metadata_model
from lib.mvc import prop_metadata_model
if(do_reload):reload(prop_metadata_model)

#prop_metadata_view
from lib.mvc import prop_metadata_view
if(do_reload):reload(prop_metadata_view)

#prop_metadata_item_delegate
from lib.mvc import prop_metadata_item_delegate
if(do_reload):reload(prop_metadata_item_delegate)

#prop_metadata_context_menu
from lib.mvc import prop_metadata_context_menu
if(do_reload):reload(prop_metadata_context_menu)


#char_metadata_model
from lib.mvc import char_metadata_model
if(do_reload):reload(char_metadata_model)

#char_metadata_view
from lib.mvc import char_metadata_view
if(do_reload):reload(char_metadata_view)

#char_metadata_item_delegate
from lib.mvc import char_metadata_item_delegate
if(do_reload):reload(char_metadata_item_delegate)

#char_metadata_context_menu
from lib.mvc import char_metadata_context_menu
if(do_reload):reload(char_metadata_context_menu)








#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = asset_manager_globals.TOOL_ROOT_PATH
MEDIA_PATH = asset_manager_globals.MEDIA_PATH
ICONS_PATH = asset_manager_globals.ICONS_PATH

#ABC_START_FRAME_OFFSET_ENABLED
ABC_START_FRAME_OFFSET_ENABLED = asset_manager_globals.ABC_START_FRAME_OFFSET_ENABLED
#ABC_START_FRAME_OFFSET
ABC_START_FRAME_OFFSET = asset_manager_globals.ABC_START_FRAME_OFFSET

#AssetManager Sizes
STACKEDWIDGET_DIVIDER_HEIGHT = asset_manager_globals.STACKEDWIDGET_DIVIDER_HEIGHT

#darkening_factor
DARKENING_FACTOR = asset_manager_globals.DARKENING_FACTOR
#brightening_factor
BRIGHTENING_FACTOR = asset_manager_globals.BRIGHTENING_FACTOR

#AssetManager colors
BRIGHT_ORANGE = asset_manager_globals.BRIGHT_ORANGE
DARK_ORANGE = asset_manager_globals.DARK_ORANGE
BRIGHT_BLUE = asset_manager_globals.BRIGHT_BLUE
DARK_BLUE = asset_manager_globals.DARK_BLUE
BRIGHT_GREEN = asset_manager_globals.BRIGHT_GREEN
DARK_GREEN = asset_manager_globals.DARK_GREEN
BRIGHT_GREY = asset_manager_globals.BRIGHT_GREY
GREY = asset_manager_globals.GREY
DARK_GREY = asset_manager_globals.DARK_GREY
DARK_BLUE = asset_manager_globals.DARK_BLUE
BRIGHT_BLUE = asset_manager_globals.BRIGHT_BLUE
WHITE = asset_manager_globals.WHITE


#AssetManager Icons
ICON_EXPORT = asset_manager_globals.ICON_EXPORT
ICON_CHAR = asset_manager_globals.ICON_CHAR
ICON_PROP = asset_manager_globals.ICON_PROP
ICON_SHOT = asset_manager_globals.ICON_SHOT
ICON_UPDATE = asset_manager_globals.ICON_UPDATE
ICON_DOCS = asset_manager_globals.ICON_DOCS

#Text
SHOT_METADATA_EXPLANATION_HEADER = asset_manager_globals.SHOT_METADATA_EXPLANATION_HEADER
SHOT_METADATA_EXPLANATION_TEXT = asset_manager_globals.SHOT_METADATA_EXPLANATION_TEXT
PROP_METADATA_EXPLANATION_HEADER = asset_manager_globals.PROP_METADATA_EXPLANATION_HEADER
PROP_METADATA_EXPLANATION_TEXT = asset_manager_globals.PROP_METADATA_EXPLANATION_TEXT
CHAR_METADATA_EXPLANATION_HEADER = asset_manager_globals.CHAR_METADATA_EXPLANATION_HEADER
CHAR_METADATA_EXPLANATION_TEXT = asset_manager_globals.CHAR_METADATA_EXPLANATION_TEXT


#UI Palette
WINDOW_COLOR = DARK_GREY#QtGui.QPalette.Window // A general background color.
BACKGROUND_COLOR = DARK_GREY#QtGui.QPalette.Background // This value is obsolete. Use Window instead.
WINDOWTEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.WindowText // A general foreground color.
FOREGROUND_COLOR = GREY#QtGui.QPalette.Foreground // This value is obsolete. Use WindowText instead.
BASE_COLOR = DARK_GREY#QtGui.QPalette.Base // Used mostly as the background color for text entry widgets, but can also be used for other painting - such as the background of combobox drop down lists and toolbar handles. It is usually white or another light color.
ALTERNATEBASE_COLOR = DARK_GREY#QtGui.QPalette.AlternateBase // Used as the alternate background color in views with alternating row colors (see QAbstractItemView.setAlternatingRowColors() ).
TOOLTIPBASE_COLOR = DARK_GREY#QtGui.QPalette.ToolTipBase // Used as the background color for PySide.QtGui.QToolTip and PySide.QtGui.QWhatsThis . Tool tips use the Inactive color group of PySide.QtGui.QPalette , because tool tips are not active windows.
TOOLTIPTEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.ToolTipText // Used as the foreground color for PySide.QtGui.QToolTip and PySide.QtGui.QWhatsThis . Tool tips use the Inactive color group of PySide.QtGui.QPalette , because tool tips are not active windows.
TEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.Text // The foreground color used with Base. This is usually the same as the WindowText, in which case it must provide good contrast with Window and Base.
BUTTON_COLOR = QtGui.QColor(QtCore.Qt.black)#QtGui.QPalette.Button // The general button background color. This background can be different from Window as some styles require a different background color for buttons.
BUTTONTEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.ButtonText // A foreground color used with the Button color.
BRIGHTTEXT_COLOR = QtGui.QColor(QtCore.Qt.black)#QtGui.QPalette.BrightText // A text color that is very different from WindowText, and contrasts well with e.g. Dark. Typically used for text that needs to be drawn where Text or WindowText would give poor contrast, such as on pressed push buttons. Note that text colors can be used for things other than just words
HIGHLIGHT_COLOR = BRIGHT_ORANGE#QtGui.QPalette.Highlight // A color to indicate a selected item or the current item. By default, the highlight color is Qt.darkBlue .
HIGHLIGHTEDTEXT_COLOR = BRIGHT_GREY#QtGui.QPalette.HighlightedText // A text color that contrasts with Highlight. By default, the highlighted text color is Qt.white .
LINK_COLOR = QtGui.QColor(QtCore.Qt.red)#QtGui.QPalette.Link // A text color used for unvisited hyperlinks. By default, the link color is Qt.blue .
LINKVISITED_COLOR = QtGui.QColor(QtCore.Qt.red)#QtGui.QPalette.LinkVisited // A text color used for already visited hyperlinks. By default, the linkvisited color is Qt.magenta .







#Cleanup old instances
#------------------------------------------------------------------

def get_widget_by_class_name_closure(wdgt_class_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_class_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_class_name from enclosing function.
        ALl this mess to be able to use it with filter.
        """
        try:
            if (type(wdgt).__name__ == wdgt_class_name):
                return True
        except:
            pass
        return False

    return get_widget_by_class_name


def get_widget_by_name_closure(wdgt_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_name from enclosing function.
        ALl this mess to be able to use it with filter.
        """
        try:
            if (wdgt.objectName() == wdgt_name):
                return True
        except:
            pass
        return False

    return get_widget_by_name


def check_and_delete_wdgt_instances_with_class_name(wdgt_class_name):
    """
    Search for all occurences with wdgt_class_name and delete them.
    """

    #get_wdgt_closure
    get_wdgt_closure = get_widget_by_class_name_closure(wdgt_class_name)

    #wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    #iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        #try to stop threads (wdgt == AssetManager)
        try:
            print('Stop threads for wdgt {0}'.format(wdgt.objectName()))
            wdgt.stop_all_threads_and_timer()
        except:
            pass

        #schedule widget for deletion
        try:
            print('Scheduled wdgt {0} for deletion'.format(wdgt.objectName()))
            #delete
            wdgt.deleteLater()
        except:
            pass

    return wdgt_list


def check_and_delete_wdgt_instances_with_name(wdgt_name):
    """
    Search for all occurences with wdgt_name and delete them.
    """

    #get_wdgt_closure
    get_wdgt_closure = get_widget_by_name_closure(wdgt_name)

    #wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    #iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        #schedule widget for deletion
        try:
            print('Scheduled wdgt {0} for deletion'.format(wdgt.objectName()))
            #delete
            wdgt.deleteLater()
        except:
            pass

    return wdgt_list













#form_class, base_class
#------------------------------------------------------------------

#ui_file
ui_file_name = 'asset_manager.ui'
ui_file = os.path.join(MEDIA_PATH, ui_file_name)

#form_class, base_class
form_class, base_class = global_functions.load_ui_type(ui_file)








#AssetManager class
#------------------------------------------------------------------
class AssetManager(form_class, base_class):
    """
    AssetManager
    """

    #Signals
    #------------------------------------------------------------------
    
    stkwdgt_change_current = QtCore.Signal(int)
    explanation_header_set_text = QtCore.Signal(str)
    explanation_text_set_text = QtCore.Signal(str)
    change_metadata_color = QtCore.Signal(QtGui.QColor)
    
    
    



    
    def __new__(cls, *args, **kwargs):
        """
        AssetManager instance factory.
        """

        #delete and cleanup old instances
        check_and_delete_wdgt_instances_with_class_name(cls.__name__)
        check_and_delete_wdgt_instances_with_class_name(asset_manager_dock_widget.AssetManagerDockWidget.__name__)

        #asset_manager_instance
        asset_manager_instance = super(AssetManager, cls).__new__(cls, args, kwargs)

        return asset_manager_instance

    
    def __init__(self, 
                logging_level = logging.DEBUG,
                auto_update_models = True,
                dock_it = True,
                show_menu = True,
                thread_interval = 2000,
                export_thread_timeout = 300,
                hide_export_shell = True,
                threads_initial_logging_level = logging.CRITICAL,
                parent = global_functions.get_main_window()):
        """
        Customize instance.
        """

        #super
        self.parent_class = super(AssetManager, self)
        self.parent_class.__init__(parent)

        #setObjectName
        self.setObjectName(self.__class__.__name__)


        #instance variables
        #------------------------------------------------------------------
        
        self.title_name = self.__class__.__name__
        self.version = 0.1
        self.title = self.title_name +' ' + str(self.version)
        self.icon_path = os.path.join(ICONS_PATH, 'icon_asset_manager.png')

        
        #maya_functionality
        self.maya_functionality = asset_manager_functionality.AssetManagerFunctionality()
        #threads_functionality
        self.threads_functionality = asset_manager_threads_functionality.AssetManagerThreadsFunctionality()
        #alembic_functionality
        self.alembic_functionality = asset_manager_alembic_functionality.AssetManagerAlembicFunctionality()
        #checks_functionality
        self.checks_functionality = asset_manager_checks.AssetManagerChecks()

        
        #auto_update_models
        self.auto_update_models = auto_update_models
        #auto_update_timer
        self.auto_update_timer = None

        #dock_it
        self.dock_it = dock_it

        #show_menu
        self.show_menu = show_menu

        #shot_metadata_list
        self.shot_metadata_list = []
        #prop_metadata_list
        self.prop_metadata_list = []
        #char_metadata_list
        self.char_metadata_list = []

        #metadata_mode
        self.metadata_mode = 'shot'

        #thread_interval
        self.thread_interval = thread_interval

        #export_thread_timeout
        self.export_thread_timeout = export_thread_timeout

        #hide_export_shell
        self.hide_export_shell = hide_export_shell

        #threads_initial_logging_level
        self.threads_initial_logging_level = threads_initial_logging_level

        #always_save_before_export
        self.always_save_before_export = None
        #never_save_before_export
        self.never_save_before_export = None

        #abc_start_frame_offset_enabled
        self.abc_start_frame_offset_enabled = ABC_START_FRAME_OFFSET_ENABLED

        #abc_start_frame_offset
        self.abc_start_frame_offset = ABC_START_FRAME_OFFSET

        

        

        
        #logger
        #------------------------------------------------------------------
        #logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        #status_handler
        self.status_handler = asset_manager_logging_handler.StatusStreamHandler(self)
        self.logger.addHandler(self.status_handler)
        

        #Init procedure
        #------------------------------------------------------------------
        
        #setupUi
        self.setupUi(self)

        #setup_additional_ui
        self.setup_additional_ui()

        #connect_ui
        self.connect_ui()

        #style_ui
        self.style_ui()

        #test_methods
        self.test_methods()

        #dock_it
        if (self.dock_it):
            self.make_dockable()

        



        

    

    
    
    
        
        
        
    
    
    
    #UI setup methods
    #------------------------------------------------------------------
    
    def setup_additional_ui(self):
        """
        Setup additional UI like mvc or helga tool header.
        """

        #make sure its floating intead of embedded
        self.setWindowFlags(QtCore.Qt.Window)

        #set title
        self.setWindowTitle(self.title)

        #setup_status_widget
        self.setup_status_widget()

        #setup_stacked_widget
        self.setup_stacked_widget() #buttons and widgets

        #setup_additional_buttons
        self.setup_additional_buttons()

        #setup_progressbar
        self.setup_progressbar()

        #setup_mvc
        self.setup_mvc()

        #show_menu
        if(self.show_menu):
            asset_manager_menu.setup_menu(self, parent = self.wdgt_menu)

        #auto_update_models
        if(self.auto_update_models):
            self.setup_auto_update_models()

        #setup_threads
        self.setup_threads()


    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        #connect_signals
        self.connect_signals()

        #connect_buttons
        self.connect_buttons()

        #connect_widgets
        self.connect_widgets()

        #connect_threads
        self.connect_threads()

        #show_menu
        if (self.show_menu):
            asset_manager_menu.connect_menu(self)

    
    def connect_signals(self):
        """
        Connect Signals for the ui.
        """

        #Signals
        self.stkwdgt_change_current.connect(self.stkwdgt_metadata.setCurrentIndex)
        self.explanation_header_set_text.connect(self.lbl_explanation_header.setText)
        self.explanation_text_set_text.connect(self.lbl_explanation_text.setText)
        self.change_metadata_color.connect(self.on_change_metadata_color)
        


    def connect_buttons(self):
        """
        Connect buttons.
        """

        #btn_docs
        self.btn_docs.clicked.connect(doc_link.run)
        
        #btn_show_shot_metadata
        self.btn_show_shot_metadata.clicked.connect(functools.partial(self.set_active_stacked_widget, self.btn_show_shot_metadata))
        self.btn_show_shot_metadata.clicked.connect(functools.partial(self.set_explanation_text, self.btn_show_shot_metadata))
        self.btn_show_shot_metadata.clicked.connect(functools.partial(self.set_metadata_color, self.btn_show_shot_metadata))
        self.btn_show_shot_metadata.clicked.connect(functools.partial(self.set_metadata_mode, 'shot'))
        #btn_show_prop_metadata
        self.btn_show_prop_metadata.clicked.connect(functools.partial(self.set_active_stacked_widget, self.btn_show_prop_metadata))
        self.btn_show_prop_metadata.clicked.connect(functools.partial(self.set_explanation_text, self.btn_show_prop_metadata))
        self.btn_show_prop_metadata.clicked.connect(functools.partial(self.set_metadata_color, self.btn_show_prop_metadata))
        self.btn_show_prop_metadata.clicked.connect(functools.partial(self.set_metadata_mode, 'prop'))
        #btn_show_char_metadata
        self.btn_show_char_metadata.clicked.connect(functools.partial(self.set_active_stacked_widget, self.btn_show_char_metadata))
        self.btn_show_char_metadata.clicked.connect(functools.partial(self.set_explanation_text, self.btn_show_char_metadata))
        self.btn_show_char_metadata.clicked.connect(functools.partial(self.set_metadata_color, self.btn_show_char_metadata))
        self.btn_show_char_metadata.clicked.connect(functools.partial(self.set_metadata_mode, 'char'))

        #btn_export
        self.btn_export.clicked.connect(self.export)

        #btn_update_models
        if not(self.auto_update_models):
            self.btn_update_models.clicked.connect(self.update_models)


    def connect_widgets(self):
        """
        Connect widgets.
        """

        #Context Menus

        #shot_metadata_view
        self.shot_metadata_view.customContextMenuRequested.connect(self.display_shot_metadata_context_menu)
        #prop_metadata_view
        self.prop_metadata_view.customContextMenuRequested.connect(self.display_prop_metadata_context_menu)
        #char_metadata_view
        self.char_metadata_view.customContextMenuRequested.connect(self.display_char_metadata_context_menu)


    def connect_threads(self):
        """
        Connect threads.
        """

        #iterate threads
        for thread in self.threads_functionality.get_thread_list():

            #connect
            thread.sgnl_task_done.connect(self.increment_progressbar)

    
    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        #correct_styled_background_attribute
        self.correct_styled_background_attribute()

        #set_margins_and_spacing
        self.set_margins_and_spacing()

        #set_active_stacked_widget 
        self.set_active_stacked_widget(self.btn_show_shot_metadata)

        #set_metadata_color
        self.set_metadata_color(self.btn_show_shot_metadata)

        #set_explanation_text
        self.set_explanation_text(self.btn_show_shot_metadata)

        #set_stylesheet
        self.setStyleSheet(asset_manager_stylesheets.get_stylesheet())

    
    def setup_status_widget(self):
        """
        Setup status widget for logging
        """

        #le_status
        self.le_status = QtGui.QLineEdit()
        self.le_status.setObjectName('le_status')
        #set in lyt
        self.lyt_status.addWidget(self.le_status)

    
    def setup_stacked_widget(self):
        """
        Setup stacked widget ui to test sweet ui design.
        """

        #setup_stacked_widget_pages
        self.setup_stacked_widget_pages()

        #setup_stacked_widget_buttons
        self.setup_stacked_widget_buttons()

    
    def setup_stacked_widget_pages(self):
        """
        Setup stacked widget pages
        """

        #wdgt_shot_metadata
        self.wdgt_shot_metadata = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(background_color_normal = DARK_GREY,
                                                                                                background_color_active = GREY,
                                                                                                parent = self)
        self.lyt_shot_metadata = QtGui.QVBoxLayout()
        self.wdgt_shot_metadata.setLayout(self.lyt_shot_metadata)
        

        #wdgt_prop_metadata
        self.wdgt_prop_metadata = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(background_color_normal = DARK_GREY,
                                                                                                background_color_active = GREY,
                                                                                                parent = self)
        self.lyt_prop_metadata = QtGui.QVBoxLayout()
        self.wdgt_prop_metadata.setLayout(self.lyt_prop_metadata)
        

        #wdgt_char_metadata
        self.wdgt_char_metadata = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(background_color_normal = DARK_GREY,
                                                                                                background_color_active = GREY,
                                                                                                parent = self)
        self.lyt_char_metadata = QtGui.QVBoxLayout()
        self.wdgt_char_metadata.setLayout(self.lyt_char_metadata)
        
        

        
        

        #stkwdgt_metadata
        self.stkwdgt_metadata =  QtGui.QStackedWidget()
        self.stkwdgt_metadata.addWidget(self.wdgt_shot_metadata)
        self.stkwdgt_metadata.addWidget(self.wdgt_prop_metadata)
        self.stkwdgt_metadata.addWidget(self.wdgt_char_metadata)
        
        #add stkwdgt_metadata to layout
        self.lyt_stacked_widget_container.addWidget(self.stkwdgt_metadata, 1, 1)


    def setup_stacked_widget_buttons(self):
        """
        Setup stacked widget buttons
        """

        #btn_show_shot_metadata
        self.btn_show_shot_metadata = asset_manager_button.AssetManagerButton( icon_name = ICON_SHOT,
                                                                                fixed_width = 64,
                                                                                fixed_height = 64,
                                                                                label_header_text = SHOT_METADATA_EXPLANATION_HEADER,
                                                                                label_text = SHOT_METADATA_EXPLANATION_TEXT,
                                                                                metadata_color_active = BRIGHT_ORANGE,
                                                                                parent = self)
        self.btn_show_shot_metadata.setObjectName('btn_show_shot_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_shot_metadata)
        #btn_show_shot_metadata_divider
        self.btn_show_shot_metadata_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                            fixed_width = 64,
                                                                                                            parent = self)
        self.btn_show_shot_metadata_divider.setObjectName('btn_show_shot_metadata_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_show_shot_metadata_divider)
        

        

        #btn_show_prop_metadata
        self.btn_show_prop_metadata = asset_manager_button.AssetManagerButton(icon_name = ICON_PROP,
                                                                                fixed_width = 64,
                                                                                fixed_height = 64,
                                                                                label_header_text = PROP_METADATA_EXPLANATION_HEADER,
                                                                                label_text = PROP_METADATA_EXPLANATION_TEXT,
                                                                                metadata_color_active = BRIGHT_BLUE,
                                                                                parent = self)
        self.btn_show_prop_metadata.setObjectName('btn_show_prop_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_prop_metadata)
        #btn_show_prop_metadata_divider
        self.btn_show_prop_metadata_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                            fixed_width = 64,
                                                                                                            parent = self)
        self.btn_show_prop_metadata_divider.setObjectName('btn_show_prop_metadata_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_show_prop_metadata_divider)
        

        

        #btn_show_char_metadata
        self.btn_show_char_metadata = asset_manager_button.AssetManagerButton(icon_name = ICON_CHAR,
                                                                                fixed_width = 64,
                                                                                fixed_height = 64,
                                                                                label_header_text = CHAR_METADATA_EXPLANATION_HEADER,
                                                                                label_text = CHAR_METADATA_EXPLANATION_TEXT,
                                                                                metadata_color_active = BRIGHT_GREEN,
                                                                                parent = self)
        self.btn_show_char_metadata.setObjectName('btn_show_char_metadata')
        self.lyt_metadata_buttons.addWidget(self.btn_show_char_metadata)
        #btn_show_char_metadata_divider
        self.btn_show_char_metadata_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                            fixed_width = 64,
                                                                                                            parent = self)
        self.btn_show_char_metadata_divider.setObjectName('btn_show_char_metadata_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_show_char_metadata_divider)


    def set_active_stacked_widget(self, wdgt_sender):
        """
        Set active stacked widget based on wdgt_sender.
        """

        #wdgt_checklist
        wdgt_checklist = [(self.btn_show_shot_metadata, self.btn_show_shot_metadata_divider, self.wdgt_shot_metadata),
                            (self.btn_show_prop_metadata, self.btn_show_prop_metadata_divider, self.wdgt_prop_metadata),
                            (self.btn_show_char_metadata, self.btn_show_char_metadata_divider, self.wdgt_char_metadata)]

        #metadata_color_active (color to differentiate shots, props, chars)
        metadata_color_active = wdgt_sender.metadata_color_active
        #metadata_color_normal (color to differentiate shots, props, chars)
        metadata_color_normal = wdgt_sender.metadata_color_normal

        #iterate and check
        for index, wdgt_list in enumerate(wdgt_checklist):
            
            for wdgt, wdgt_divider, wdgt_metadata in [wdgt_list]:
            
                #if match set active
                if (wdgt is wdgt_sender):

                    #set stylesheets

                    #wdgt
                    wdgt.set_hover_radial_color_active(metadata_color_active)
                    wdgt.set_stylesheet(role = 'active')
                    
                    #wdgt_divider
                    wdgt_divider.set_background_color_active(metadata_color_active)
                    wdgt_divider.set_stylesheet(role = 'active')
                    
                    #wdgt_metadata
                    wdgt_metadata.set_stylesheet(role = 'active')

                    #btn_docs
                    self.btn_docs.set_background_color_normal(metadata_color_active.darker(DARKENING_FACTOR))
                    self.btn_docs.set_stylesheet(role = 'normal')

                    #btn_export
                    self.btn_export.set_hover_radial_color_normal(metadata_color_active)
                    self.btn_export.set_stylesheet(role = 'normal')

                    #btn_update_models
                    if not(self.auto_update_models):
                        self.btn_update_models.set_hover_radial_color_normal(metadata_color_active)
                        self.btn_update_models.set_stylesheet(role = 'normal')

                    #emit changed
                    self.stkwdgt_change_current.emit(index) #sets active widget

                #else normal
                else:

                    #set_stylesheets

                    #wdgt
                    wdgt.set_hover_radial_color_normal(metadata_color_active)
                    wdgt.set_stylesheet(role = 'normal')

                    #wdgt_divider
                    wdgt_divider.set_background_color_normal(metadata_color_normal)
                    wdgt_divider.set_stylesheet(role = 'normal')
                    
                    #wdgt_metadata
                    wdgt_metadata.set_stylesheet(role = 'normal')


    def set_explanation_text(self, wdgt_sender):
        """
        Set explanation text. Means setting the text for self.lbl_explanation_header
        and self.lbl_explanation_text.
        """

        #wdgt_checklist
        wdgt_checklist = [self.btn_show_shot_metadata, 
                            self.btn_show_prop_metadata, 
                            self.btn_show_char_metadata]

        #iterate and check
        for index, wdgt in enumerate(wdgt_checklist):
            
            #if match set text
            if (wdgt is wdgt_sender):

                #emit
                self.explanation_header_set_text.emit(wdgt_sender.label_header_text)
                self.explanation_text_set_text.emit(wdgt_sender.label_text)


    def set_metadata_color(self, wdgt_sender):
        """
        Set color of some widgets based on the current metadata mode.
        This mode can be either shots, props or characters.
        The needed color comes from wdgt_sender.
        Time will tell if that was a good idea....
        """

        #wdgt_checklist
        wdgt_checklist = [self.btn_show_shot_metadata, 
                            self.btn_show_prop_metadata, 
                            self.btn_show_char_metadata]

        #iterate and check
        for index, wdgt in enumerate(wdgt_checklist):
            
            #if match set text
            if (wdgt is wdgt_sender):

                #emit
                self.change_metadata_color.emit(wdgt_sender.metadata_color_active)


    def correct_styled_background_attribute(self):
        """
        Set QtCore.Qt.WA_StyledBackground True for all widgets.
        Without this attr. set, the background-color stylesheet
        will have no effect on QWidgets. This should replace the
        need for palette settings.
        ToDo:
        Maybe add exclude list when needed.
        """

        #wdgt_list
        wdgt_list = self.findChildren(QtGui.QWidget) #Return several types ?!?!

        #iterate and set
        for wdgt in wdgt_list:
            
            #check type
            if(type(wdgt) is QtGui.QWidget):

                #styled_background
                wdgt.setAttribute(QtCore.Qt.WA_StyledBackground, True)



    def set_margins_and_spacing(self):
        """
        Eliminate margin and spacing for all layout widgets.
        """

        #margin_list
        margin_list = [0,0,0,0]

        #lyt_classes_list
        lyt_classes_list = [QtGui.QStackedLayout, QtGui.QGridLayout, QtGui.QFormLayout, 
                            QtGui.QBoxLayout, QtGui.QVBoxLayout, QtGui.QHBoxLayout, QtGui.QBoxLayout]

        #lyt_list
        lyt_list = []
        for lyt_class in lyt_classes_list:
            lyt_list += [wdgt for wdgt in self.findChildren(lyt_class)]


        
        #set margin and spacing
        for lyt in lyt_list:

            #check type
            if(type(lyt) in lyt_classes_list):

                #set
                lyt.setContentsMargins(*margin_list)
                lyt.setSpacing(0)


    def setup_tool_palette_global(self):
        """
        Setup palette for tool and apply to all widgets.
        This should be applied before all unique customizations
        and stylesheets.
        """

        #wdgt_list
        wdgt_list = self.findChildren(QtCore.QObject)

        #customize palette
        for wdgt in wdgt_list:
            
            try:
                self.customize_palette(wdgt, QtGui.QPalette.Window, WINDOW_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Background, BACKGROUND_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.WindowText, WINDOWTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Foreground, FOREGROUND_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Base, BASE_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.AlternateBase, ALTERNATEBASE_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.ToolTipBase, TOOLTIPBASE_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.ToolTipText, TOOLTIPTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Text, TEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Button, BUTTON_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.ButtonText, BUTTONTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.BrightText, BRIGHTTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Highlight, HIGHLIGHT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.HighlightedText, HIGHLIGHTEDTEXT_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.Link, LINK_COLOR)
                self.customize_palette(wdgt, QtGui.QPalette.LinkVisited, LINKVISITED_COLOR)
            
            except:
                pass


    def setup_tool_palette_specific(self):
        """
        Setup the palette for specific widgets.
        Mostly needed for QWidgets that refuse to
        accepts background_color stylesheets
        """

        pass


    def setup_additional_buttons(self):
        """
        Setup additional buttons anywhere in the tool.
        """

        #setup_model_update_button
        if not(self.auto_update_models):
            self.setup_model_update_button()

        #setup_export_button
        self.setup_export_button()

        #setup_docs_button
        self.setup_docs_button()


    def setup_export_button(self):
        """
        Create self.btn_export
        """

        #btn_export
        self.btn_export = asset_manager_button.AssetManagerButton(icon_name = ICON_EXPORT,
                                                                    fixed_width = 64,
                                                                    fixed_height = 64,
                                                                    parent = self)
        self.btn_export.setObjectName('btn_export')
        self.lyt_metadata_buttons.addWidget(self.btn_export)
        #btn_export_divider
        self.btn_export_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                fixed_width = 64,
                                                                                                parent = self)
        self.btn_export_divider.setObjectName('btn_export_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_export_divider)


    def setup_model_update_button(self):
        """
        Create self.btn_update_models
        """

        #btn_update_models
        self.btn_update_models = asset_manager_button.AssetManagerButton(icon_name = ICON_UPDATE,
                                                                            fixed_width = 64,
                                                                            fixed_height = 64,
                                                                            parent = self)
        self.btn_update_models.setObjectName('btn_update_models')
        self.lyt_metadata_buttons.addWidget(self.btn_update_models)
        #btn_update_models_divider
        self.btn_update_models_divider = asset_manager_stylesheet_widget.AssetManagerStylesheetWidget(fixed_height = STACKEDWIDGET_DIVIDER_HEIGHT,
                                                                                                            fixed_width = 64,
                                                                                                            parent = self)
        self.btn_update_models_divider.setObjectName('btn_update_models_divider')
        self.lyt_metadata_buttons.addWidget(self.btn_update_models_divider)


    def setup_docs_button(self):
        """
        Create self.btn_docs
        """

        #btn_docs
        self.btn_docs = asset_manager_button.AssetManagerButton(icon_name = ICON_DOCS,
                                                                background_color_normal = DARK_ORANGE,
                                                                hover_radial_color_normal = WHITE,
                                                                hover_radial_radius = 0.4,
                                                                fixed_width = 64,
                                                                fixed_height = 64,
                                                                parent = self)
        self.btn_docs.setObjectName('btn_docs')
        self.lyt_docs.addWidget(self.btn_docs)
        


    def setup_progressbar(self):
        """
        Setup self.progressbar.
        """

        #progressbar
        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setObjectName('progressbar')
        #customize
        self.progressbar.setTextVisible(True)
        self.progressbar.setOrientation(QtCore.Qt.Vertical)
        self.progressbar.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        #set min, max and reset
        self.progressbar.setRange(0, 1)
        self.progressbar.setValue(0)

        #add to lyt
        self.lyt_metadata_progress.addWidget(self.progressbar)

        #log
        self.logger.debug('Progressbar range: {0} - {1}'.format(self.progressbar.minimum(), 
                                                                self.progressbar.maximum()))
        
    
    def setup_mvc(self):
        """
        Setup all model-view controller.
        """

        #setup_mvc_shot_metadata
        self.setup_mvc_shot_metadata()

        #setup_mvc_prop_metadata
        self.setup_mvc_prop_metadata()

        #setup_mvc_char_metadata
        self.setup_mvc_char_metadata()


    def setup_mvc_shot_metadata(self):
        """
        Setup model-view controller for shot metadata.
        """
    
        #shot_metadata_view
        self.shot_metadata_view = shot_metadata_view.ShotMetadataView(self.logging_level)
        self.shot_metadata_view.setWordWrap(True)
        #set resize mode for horizontal header
        self.shot_metadata_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.shot_metadata_view.horizontalHeader().setStretchLastSection(False)
        self.shot_metadata_view.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.shot_metadata_view.setAlternatingRowColors(True)
        #objectNames
        self.shot_metadata_view.setObjectName('shot_metadata_view')
        self.shot_metadata_view.horizontalHeader().setObjectName('shot_metadata_view_hor_header')
        self.shot_metadata_view.verticalHeader().setObjectName('shot_metadata_view_ver_header')
        #context menu
        self.shot_metadata_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #add to ui
        self.lyt_shot_metadata.addWidget(self.shot_metadata_view)


        #shot_metadata_item_delegate
        self.shot_metadata_item_delegate = shot_metadata_item_delegate.ShotMetadataItemDelegate(self.logging_level)
        self.shot_metadata_item_delegate.setObjectName('shot_metadata_item_delegate')
        #set in view
        self.shot_metadata_view.setItemDelegate(self.shot_metadata_item_delegate)

        
        #shot_metadata_model
        self.shot_metadata_model = shot_metadata_model.ShotMetadataModel(self.logging_level)
        #set model in view
        self.shot_metadata_view.setModel(self.shot_metadata_model)

        #shot_metadata_selection_model
        self.shot_metadata_selection_model = QtGui.QItemSelectionModel(self.shot_metadata_model)
        self.shot_metadata_view.setSelectionModel(self.shot_metadata_selection_model)


        #After everything is set, hide items
        
        #hide vertical header
        self.shot_metadata_view.verticalHeader().hide()
        #hide alembic_path column
        self.shot_metadata_view.view_functionality.hide_column_with_header_name('Alembic Path', True)
        
    
    def display_shot_metadata_context_menu(self, pos):
        """
        Create and display shot metadata context menu.
        """
        
        #context_menu
        context_menu = shot_metadata_context_menu.ShotMetadataContextMenu(parent = self)
        context_menu.set_view(self.shot_metadata_view)
        context_menu.popup(self.shot_metadata_view.mapToGlobal(pos))


    def setup_mvc_prop_metadata(self):
        """
        Setup model-view controller for prop metadata.
        """
    
        #prop_metadata_view
        self.prop_metadata_view = prop_metadata_view.PropMetadataView(self.logging_level)
        self.prop_metadata_view.setWordWrap(True)
        #set resize mode for horizontal header
        self.prop_metadata_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.prop_metadata_view.horizontalHeader().setStretchLastSection(False)
        self.prop_metadata_view.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.prop_metadata_view.setAlternatingRowColors(True)
        #objectNames
        self.prop_metadata_view.setObjectName('prop_metadata_view')
        self.prop_metadata_view.horizontalHeader().setObjectName('prop_metadata_view_hor_header')
        self.prop_metadata_view.verticalHeader().setObjectName('prop_metadata_view_ver_header')
        #context menu
        self.prop_metadata_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #add to ui
        self.lyt_prop_metadata.addWidget(self.prop_metadata_view)

        
        #prop_metadata_item_delegate
        self.prop_metadata_item_delegate = prop_metadata_item_delegate.PropMetadataItemDelegate(self.logging_level)
        self.prop_metadata_item_delegate.setObjectName('prop_metadata_item_delegate')
        #set in view
        self.prop_metadata_view.setItemDelegate(self.prop_metadata_item_delegate)
        

        
        #prop_metadata_model
        self.prop_metadata_model = prop_metadata_model.PropMetadataModel(self.logging_level)
        #set model in view
        self.prop_metadata_view.setModel(self.prop_metadata_model)

        #prop_metadata_selection_model
        self.prop_metadata_selection_model = QtGui.QItemSelectionModel(self.prop_metadata_model)
        self.prop_metadata_view.setSelectionModel(self.prop_metadata_selection_model)


        #After everything is set, hide items
        
        #hide vertical header
        self.prop_metadata_view.verticalHeader().hide()

        #hide ExportProxy column
        self.prop_metadata_view.view_functionality.hide_column_with_header_name('ExportProxy', True)
        #hide ExportLocator column
        self.prop_metadata_view.view_functionality.hide_column_with_header_name('ExportLocator', True)


    def display_prop_metadata_context_menu(self, pos):
        """
        Create and display prop metadata context menu.
        """
        
        #context_menu
        context_menu = prop_metadata_context_menu.PropMetadataContextMenu(parent = self)
        context_menu.set_view(self.prop_metadata_view)
        context_menu.popup(self.prop_metadata_view.mapToGlobal(pos))


    def setup_mvc_char_metadata(self):
        """
        Setup model-view controller for char metadata.
        """
    
        #char_metadata_view
        self.char_metadata_view = char_metadata_view.CharMetadataView(self.logging_level)
        self.char_metadata_view.setWordWrap(True)
        #set resize mode for horizontal header
        self.char_metadata_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.char_metadata_view.horizontalHeader().setStretchLastSection(False)
        self.char_metadata_view.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.char_metadata_view.setAlternatingRowColors(True)
        #objectNames
        self.char_metadata_view.setObjectName('char_metadata_view')
        self.char_metadata_view.horizontalHeader().setObjectName('char_metadata_view_hor_header')
        self.char_metadata_view.verticalHeader().setObjectName('char_metadata_view_ver_header')
        #context menu
        self.char_metadata_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #add to ui
        self.lyt_char_metadata.addWidget(self.char_metadata_view)

        
        #char_metadata_item_delegate
        self.char_metadata_item_delegate = char_metadata_item_delegate.CharMetadataItemDelegate(self.logging_level)
        self.char_metadata_item_delegate.setObjectName('char_metadata_item_delegate')
        #set in view
        self.char_metadata_view.setItemDelegate(self.char_metadata_item_delegate)
        

        
        #char_metadata_model
        self.char_metadata_model = char_metadata_model.CharMetadataModel(self.logging_level)
        #set model in view
        self.char_metadata_view.setModel(self.char_metadata_model)

        #char_metadata_selection_model
        self.char_metadata_selection_model = QtGui.QItemSelectionModel(self.char_metadata_model)
        self.char_metadata_view.setSelectionModel(self.char_metadata_selection_model)


        #After everything is set, hide items
        
        #hide vertical header
        self.char_metadata_view.verticalHeader().hide()
        #hide ExportProxy column
        self.char_metadata_view.view_functionality.hide_column_with_header_name('ExportProxy', True)
        #hide ExportLocator column
        self.char_metadata_view.view_functionality.hide_column_with_header_name('ExportLocator', True)


    def display_char_metadata_context_menu(self, pos):
        """
        Create and display char metadata context menu.
        """
        
        #context_menu
        context_menu = char_metadata_context_menu.CharMetadataContextMenu(parent = self)
        context_menu.set_view(self.char_metadata_view)
        context_menu.popup(self.char_metadata_view.mapToGlobal(pos))



    #MVC methods
    #------------------------------------------------------------------

    def convert_list_for_tablemodel(self, list_to_convert):
        """
        [obj, obj, obj] >> [[obj], [obj], [obj]]
        """

        #list false
        if not (list_to_convert):
            return [[]]

        #table_model_list
        table_model_list = [[pynode] for pynode in list_to_convert]

        return table_model_list


    def setup_auto_update_models(self, interval = 2000):
        """
        Create QTimer to automatically trigger update_models in intervals.
        """

        #auto_update_timer
        self.auto_update_timer = QtCore.QTimer(self)
        self.auto_update_timer.timeout.connect(self.update_models)
        self.auto_update_timer.start(interval)

    
    def update_models(self):
        """
        Update all models.
        """

        #update if neccessary
        if (self.update_models_necessary()):

            #log
            print('Update models: {0}'.format(time.time()))
            
            #update_shotmetadata_model
            self.update_shotmetadata_model()

            #update_propmetadata_model
            self.update_propmetadata_model()

            #update_charmetadata_model
            self.update_charmetadata_model()


    def get_hashstring_from_list(self, list_to_convert):
        """
        Convert a list to a hashable string.
        """

        #hashable_string
        hashable_string = self.maya_functionality.get_maya_file()
        
        #If no file given (for example when a new file is opened)
        #create a random string to avoid matching with the empty string
        #given by the empty list concatenation from the scene metadata node check
        if not(hashable_string):
            hashable_string = 'new_file'

        #if list_to_convert empty
        if not (list_to_convert):
            return hashable_string

        #check if all nodes still exist
        if not(all([pynode.exists() for pynode in list_to_convert])):
            hashable_string += 'missing_pynodes'
            return hashable_string
        
        try:
            
            #sorted_list
            sorted_list = sorted([pynode.name() for pynode in list_to_convert])

            #iterate and concatenate
            for name in sorted_list:
                hashable_string += name

            
            return hashable_string

        except:
            pass
        
        #return
        return hashable_string


    def update_models_necessary(self):
        """
        Hash and check model metadata lists and 
        decide if update_models() is necessary.
        """

        #model data

        #shot_metadata_list_string
        shot_metadata_list_string = self.get_hashstring_from_list(self.shot_metadata_list)
        #prop_metadata_list_string
        prop_metadata_list_string = self.get_hashstring_from_list(self.prop_metadata_list)
        #char_metadata_list_string
        char_metadata_list_string = self.get_hashstring_from_list(self.char_metadata_list)

        #current_metadata_lists_string
        current_metadata_lists_string = shot_metadata_list_string + prop_metadata_list_string + char_metadata_list_string
        current_metadata_lists_string = str(current_metadata_lists_string)
        

        #current_metadata_lists_hash_object
        current_metadata_lists_hash_object = hashlib.sha1(bytearray(current_metadata_lists_string))
        current_model_lists_hex_digest = current_metadata_lists_hash_object.hexdigest()
        


        #scene data
        
        #new_shot_metadata_list
        new_shot_metadata_list = self.maya_functionality.get_nodes_of_type('HelgaShotsMetadata')
        #new_prop_metadata_list
        new_prop_metadata_list = self.maya_functionality.get_nodes_of_type('HelgaPropMetadata')
        #new_char_metadata_list
        new_char_metadata_list = self.maya_functionality.get_nodes_of_type('HelgaCharacterMetadata')

        #new_shot_metadata_list_string
        new_shot_metadata_list_string = self.get_hashstring_from_list(new_shot_metadata_list)
        #new_prop_metadata_list_string
        new_prop_metadata_list_string = self.get_hashstring_from_list(new_prop_metadata_list)
        #new_char_metadata_list_string
        new_char_metadata_list_string = self.get_hashstring_from_list(new_char_metadata_list)

        #new_metadata_lists_string
        new_metadata_lists_string = new_shot_metadata_list_string + new_prop_metadata_list_string + new_char_metadata_list_string
        new_metadata_lists_string = str(new_metadata_lists_string)
        

        #new_metadata_lists_hash_object
        new_metadata_lists_hash_object = hashlib.sha1(bytearray(new_metadata_lists_string))
        new_model_lists_hex_digest = new_metadata_lists_hash_object.hexdigest()
        


        #compare and return
        if(new_model_lists_hex_digest == current_model_lists_hex_digest):
            return False

        return True


    def update_shotmetadata_model(self):
        """
        Update self.shot_metadata_model
        """

        #set_shot_metadata_list from scene
        self.set_shot_metadata_list()

        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.shot_metadata_list)

        #set in model
        self.shot_metadata_model.update(table_model_list)


    def update_propmetadata_model(self):
        """
        Update self.prop_metadata_model
        """

        #set_prop_metadata_list from scene
        self.set_prop_metadata_list()

        
        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.prop_metadata_list)

        #set in model
        self.prop_metadata_model.update(table_model_list)
        


    def update_charmetadata_model(self):
        """
        Update self.char_metadata_model
        """

        #set_char_metadata_list from scene
        self.set_char_metadata_list()

        
        #list_for_tablemodel
        table_model_list = self.convert_list_for_tablemodel(self.char_metadata_list)

        #set in model
        self.char_metadata_model.update(table_model_list)
        






    

    


    #Threads
    #------------------------------------------------------------------
        
    def setup_threads(self):
        """
        Setup threads.
        """

        #start threads
        self.threads_functionality.setup_threads(thread_interval = self.thread_interval, 
                                                    logging_level = self.threads_initial_logging_level)

        




    


    #Getter & Setter
    #------------------------------------------------------------------

    @QtCore.Slot(str)
    def set_status(self, new_value):
        """
        Set le_status text
        """
        try:
            
            #clear
            self.le_status.clear()
            #set text
            self.le_status.setText(new_value)

        except:

            pass
        

    def get_status(self):
        """
        Return content of le_status
        """

        try:
            return str(self.le_status.text())
        except:
            pass


    def customize_palette(self, wdgt, role, color):
        """
        Set background color for widget.
        """

        #setAutoFillBackground
        try:
            if(role == wdgt.backgroundRole()):
                wdgt.setAutoFillBackground(True)
        except:
            pass
        
        try:
            
            #palette_to_customize
            palette_to_customize = wdgt.palette()
            #set color
            palette_to_customize.setColor(role, color)
            wdgt.setPalette(palette_to_customize)
        
        except:

            #log
            self.logger.debug('Error setting palette for {0} - {1}'.format(wdgt.objectName(), wdgt))



    def set_shot_metadata_list(self):
        """
        Set self.shot_metadata_list
        """
        
        self.shot_metadata_list = self.maya_functionality.get_nodes_of_type('HelgaShotsMetadata')


    def set_prop_metadata_list(self):
        """
        Set self.prop_metadata_list
        """
        
        self.prop_metadata_list = self.maya_functionality.get_nodes_of_type('HelgaPropMetadata')


    def set_char_metadata_list(self):
        """
        Set self.char_metadata_list
        """
        
        self.char_metadata_list = self.maya_functionality.get_nodes_of_type('HelgaCharacterMetadata')


    def get_metadata_mode(self):
        """
        Return self.metadata_mode
        """

        return self.metadata_mode


    def set_metadata_mode(self, value):
        """
        Set self.metadata_mode
        """

        self.metadata_mode = value


    def get_random_string(self, 
                            size = 12, 
                            chars = string.ascii_uppercase + string.digits):
        """
        Create and return a random string.
        """

        return ''.join(random.choice(chars) for _ in range(size))


    def get_thread_interval(self):
        """
        Get self.thread_interval
        """

        return self.thread_interval


    @QtCore.Slot(int)
    def set_export_thread_timeout(self, value):
        """
        Set self.export_thread_timeout to value
        """

        #set
        self.export_thread_timeout = value

        #log
        self.logger.debug('Set export_thread_timeout to {0}'.format(self.export_thread_timeout))


    def get_export_thread_timeout(self):
        """
        Get self.export_thread_timeout
        """

        return self.export_thread_timeout


    @QtCore.Slot(bool)
    def set_hide_export_shell(self, value):
        """
        Set self.hide_export_shell to value
        """

        #set
        self.hide_export_shell = value

        #log
        self.logger.debug('Set hide_export_shell to {0}'.format(self.hide_export_shell))


    def get_hide_export_shell(self):
        """
        Get self.hide_export_shell
        """

        return self.hide_export_shell


    @QtCore.Slot(float)
    def set_abc_start_frame_offset(self, value):
        """
        Set self.abc_start_frame_offset
        """
        
        self.abc_start_frame_offset = value

        #log
        self.logger.debug('Set abc_start_frame_offset to {0}'.format(self.get_abc_start_frame_offset()))


    def get_abc_start_frame_offset(self):
        """
        Get self.abc_start_frame_offset
        """
        
        return self.abc_start_frame_offset


    @QtCore.Slot(bool)
    def set_abc_start_frame_offset_enabled(self, value):
        """
        Set self.abc_start_frame_offset_enabled
        """
        
        self.abc_start_frame_offset_enabled = value

        #log
        self.logger.debug('Set abc_start_frame_offset_enabled to {0}'.format(self.get_abc_start_frame_offset_enabled()))


    def get_abc_start_frame_offset_enabled(self):
        """
        Get self.abc_start_frame_offset_enabled
        """
        
        return self.abc_start_frame_offset_enabled






    #Slots
    #------------------------------------------------------------------

    @QtCore.Slot(QtGui.QColor)
    def on_change_metadata_color(self, metadata_color):
        """
        Set stylesheets for widgets to background with
        metadata_color.
        """
        
        #set_stylesheet_wdgt_docs
        self.set_stylesheet_wdgt_docs(metadata_color)

        #set_stylesheet_le_status
        self.set_stylesheet_le_status(metadata_color)

        #set_stylesheet_wdgt_explanation
        self.set_stylesheet_wdgt_explanation(metadata_color)

        #set_stylesheet_progressbar
        self.set_stylesheet_progressbar(metadata_color)


    def set_stylesheet_wdgt_docs(self, metadata_color):
        """
        Set stylesheet for self.wdgt_docs
        """

        #ss_dict
        ss_dict = {'metadata_color' : metadata_color.darker(DARKENING_FACTOR).name()}

        #str_stylesheet
        str_stylesheet = " \
            /* QWidget - wdgt_docs */\
            QWidget#wdgt_docs { background-color: %(metadata_color)s; } \
        "%ss_dict
        
        #set
        self.wdgt_docs.setStyleSheet(str_stylesheet)


    def set_stylesheet_le_status(self, metadata_color):
        """
        Set stylesheet for self.le_status
        """

        #ss_dict
        ss_dict = {'metadata_color' : metadata_color.name(),
                    'metadata_color_darker' : metadata_color.darker(DARKENING_FACTOR).name(),
                    'bright_grey' : BRIGHT_GREY.name(),
                    'grey' : GREY.name(),
                    'stackwidget_divider_height': STACKEDWIDGET_DIVIDER_HEIGHT - STACKEDWIDGET_DIVIDER_HEIGHT} #remove minus to enable it

        #str_stylesheet
        str_stylesheet = " \
            /* QLineEdit - le_status*/\
            QLineEdit#le_status { border: none; \
                                    background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, \
                                    stop:0 %(metadata_color_darker)s, \
                                    stop:1 %(metadata_color)s); \
                                    color: %(bright_grey)s; \
                                    border-left: none; \
                                    border-top: %(stackwidget_divider_height)spx solid %(grey)s; \
                                    border-bottom: none; \
                                    border-right: none; \
        } \
        "%ss_dict
        
        #set
        self.le_status.setStyleSheet(str_stylesheet)


    def set_stylesheet_wdgt_explanation(self, metadata_color):
        """
        Set stylesheet for self.wdgt_explanation
        """

        #ss_dict
        ss_dict = {'metadata_color' : metadata_color.name(),
                    'metadata_color_brighter' : metadata_color.lighter(BRIGHTENING_FACTOR).name()}

        #str_stylesheet
        str_stylesheet = " \
            /* QWidget - wdgt_explanation */\
            QWidget#wdgt_explanation { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \
                                        stop:0 %(metadata_color)s, \
                                        stop:1 %(metadata_color_brighter)s); \
                                        } \
                                        \
        "%ss_dict
        
        #set
        self.wdgt_explanation.setStyleSheet(str_stylesheet)


    def set_stylesheet_progressbar(self, metadata_color):
        """
        Set stylesheet for self.progressbar
        """

        #ss_dict
        ss_dict = {'metadata_color' : metadata_color.name(),
                    'metadata_color_brighter' : metadata_color.lighter(BRIGHTENING_FACTOR).name()}

        #str_stylesheet
        str_stylesheet = " \
            /* QProgressBar - chunk */\
            QProgressBar::chunk { border: none;\
                                    background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, \
                                    stop:0 %(metadata_color)s, \
                                    stop:1 %(metadata_color_brighter)s); \
            } \
        "%ss_dict
        
        #set
        self.progressbar.setStyleSheet(str_stylesheet)


    @QtCore.Slot()
    def increment_progressbar(self, step_size = 1):
        """
        Increment self.progressbar by step_size.
        """

        #current_value
        current_value = self.progressbar.value()
        #if zero set to 1 for more readable maximum checking
        if not (current_value):
            current_value = 1

        #incremented_value
        incremented_value = current_value + step_size

        
        #progressbar full (This should be true on the last job_done signal)
        if (incremented_value == self.progressbar.maximum()):

            #set range
            self.progressbar.setRange(0, 1)
            #reset
            self.progressbar.setValue(0)

            #log
            self.logger.debug('Progressbar reset.')

            #return
            return


        #set
        self.progressbar.setValue(incremented_value)

        #log
        self.logger.debug('Progressbar value: {0}'.format(self.progressbar.value()))


    @QtCore.Slot()
    def increment_progressbar_range(self, step_size = 1):
        """
        Increment progressbar maximum by one.
        Keep minimum unaffected.
        """

        #current_maximum
        current_maximum = self.progressbar.maximum()

        #incremented_maximum
        incremented_maximum = current_maximum + step_size

        #set range
        self.progressbar.setRange(0, incremented_maximum)

        #log
        self.logger.debug('Progressbar range: {0} - {1}'.format(self.progressbar.minimum(), 
                                                                self.progressbar.maximum()))


    




    #Events
    #------------------------------------------------------------------

    def stop_all_threads_and_timer(self):
        """
        Try to stop all threads and timers that AssetManager started.
        This method is ment to be used in a closeEvent.
        """
        
        try:
            
            #stop timer
            if(self.auto_update_timer):
                self.auto_update_timer.stop()

        except:

            #log
            self.logger.debug('Error stopping auto update timer.')


        try:
            
            #stop threads
            self.threads_functionality.stop_threads()

        except:

            #log
            self.logger.debug('Error stopping threads for queue.')

        


    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        #log
        self.logger.debug('Close Event')

        #stop_all_threads_and_timer
        self.stop_all_threads_and_timer()

        #parent close event
        self.parent_class.closeEvent(event)


    




    


    #Docking
    #------------------------------------------------------------------

    def make_dockable(self):
        """
        Make this window dockable.
        """

        #maya_main_window
        maya_main_window = global_functions.get_main_window()

        #wdgt_dock
        self.wdgt_dock = asset_manager_dock_widget.AssetManagerDockWidget(parent = maya_main_window)
        self.wdgt_dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)

        #set title
        #self.wdgt_dock.setWindowTitle(self.title)

        #set wdgt
        self.wdgt_dock.setWidget(self)
        
        #add to maya main window
        maya_main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.wdgt_dock)

        
        

        




    






    



    #Export
    #------------------------------------------------------------------

    def run_pre_export_dialog(self):
        """
        Run the pre export save dialog.
        This dialog lets you pick if you want to save before export.
        You can also choose to remember your pick. In this case the
        dialog will still be run but not shown. (Thats why this method is
        named run instead of display or show). 
        """

        #always save
        if(self.always_save_before_export):

            #log
            self.logger.debug('Always save scene before export')
            
            #save
            self.maya_functionality.save_scene()
            return
        
        #never save
        elif(self.never_save_before_export):

            #log
            self.logger.debug('Never save scene before export')
            
            return
        
        #display dialog
        else:
            
            #pre_export_dialog
            pre_export_dialog = asset_manager_pre_export_dialog.AssetManagerPreExportDialog(question = 'Save before export?\n(Unsaved animation is not exported.)',
                                                                                            parent = self)

            #do_save
            do_save = pre_export_dialog.exec_()

            #remember_choice
            if(pre_export_dialog.get_remember_choice()):
                
                #always save
                if (do_save):

                    #save always
                    self.always_save_before_export = True
                    
                    #save
                    self.maya_functionality.save_scene()

                #never save
                else:

                    #save never
                    self.never_save_before_export = True
                    


            #dont remember
            else:
                
                #save
                if (do_save):

                    #save
                    self.maya_functionality.save_scene()


    def export(self, dry_run = False):
        """
        Export Alembic. This function is called when the export button is pressed.
        If dry_run is True, only print the export command.
        """

        #Get and check base data
        #------------------------------------------------------------------

        #maya_file
        maya_file = self.maya_functionality.get_maya_file()
        #file exists
        if not(os.path.isfile(maya_file)):
            #log
            self.logger.debug('Maya file {0} does not exist. Not exporting.'.format(maya_file))
            return

        
        #node_list
        node_list = self.shot_metadata_model.get_data_list_flat()
        #check node_list len
        if not(len(node_list) == 1):
            #log
            self.logger.debug('No or too many shot metatdata nodes. Please make sure there is only one. Not exporting.')
            return

        #shot_metadata_node
        shot_metadata_node = node_list[0]

        
        #run checks on base data
        if not(self.checks_functionality.check_base_data(shot_metadata_node)):
            #log
            self.logger.debug('Base data check failed. Check shot name, alembic path, shot start and end settings. Not exporting.')
            return


        
        #run_pre_export_dialog
        if not(dry_run):
            self.run_pre_export_dialog()
        

        
        
        #metadata_mode
        metadata_mode = self.get_metadata_mode()

        #Shot
        #------------------------------------------------------------------

        if (metadata_mode == 'shot'):

            #fake loop to simulate same behaviour as for other modes
            for shot_metadata_node in [shot_metadata_node]:
                
                #export
                self.export_shot_cam(shot_metadata_node, dry_run)


        
        #Prop
        #------------------------------------------------------------------

        elif (metadata_mode == 'prop'):

            #prop_metadata_node_list
            prop_metadata_node_list = self.prop_metadata_model.get_data_list_flat()
            #check prop_metadata_node_list len
            if not(prop_metadata_node_list):
                #log
                self.logger.debug('Prop metadata node list empty. Not exporting.')
                return

            
            #iterate
            for prop_metadata_node in prop_metadata_node_list:

                #export
                self.export_prop(shot_metadata_node, prop_metadata_node, dry_run)

        

        #Char
        #------------------------------------------------------------------
        
        elif (metadata_mode == 'char'):

            #char_metadata_node_list
            char_metadata_node_list = self.char_metadata_model.get_data_list_flat()
            #check char_metadata_node_list len
            if not(char_metadata_node_list):
                #log
                self.logger.debug('Char metadata node list empty. Not exporting.')
                return

            
            #iterate
            for char_metadata_node in char_metadata_node_list:

                #export
                self.export_char(shot_metadata_node, char_metadata_node, dry_run)


    def export_shot_cam(self, 
                        shot_metadata_node,  
                        dry_run):
        """
        Export shot cam.
        Base data checks have passed at this point so its save to
        retrieve the base data from the shot_metadata_node again.
        """

        #run checks shot data
        if not(self.checks_functionality.check_shot_data(shot_metadata_node)):
            
            #log
            self.logger.debug('Shot data check failed. Check shot cam settings. Not exporting.')
            return

        

        #shot_cam
        shot_cam = self.checks_functionality.check_shot_data(shot_metadata_node)


        #alembic_path, shot_start, shot_end
        alembic_path, shot_start, shot_end = self.checks_functionality.check_base_data(shot_metadata_node)

        #start frame offset enabled
        if (self.get_abc_start_frame_offset_enabled()):
            
            #shot_start + offset (Offset is negative by default)
            shot_start = shot_start + self.get_abc_start_frame_offset()
        
        
        #alembic_export_path
        alembic_subdir = 'cameras'
        asset_name = 'shot_cam'
        alembic_export_path = alembic_path +'/' +alembic_subdir +'/' +asset_name +'.abc'

        
        #abc_command
        abc_command = self.alembic_functionality.build_export_command([shot_cam], 
                                                                        [shot_start, shot_end], 
                                                                        alembic_export_path)
        
        #env_dict
        env_dict = self.get_env_dict(shot_metadata_node)
        #add abc_command
        env_dict.setdefault('HELGA_ABC_COMMAND', abc_command)

        
        #dry_run
        if(dry_run):

            #log
            self.logger.debug('{0}'.format(abc_command))
            
        #no dry_run
        else:
            
            #get closure and add to thread queue
            self.add_export_closure_to_queue(env_dict)


    def export_prop(self, 
                    shot_metadata_node, 
                    prop_metadata_node, 
                    dry_run):
        """
        Export prop for given prop_metadata_node.
        Base data checks have passed at this point so its save to
        pass the shot_metadata_node and retrieve its values
        again.
        """

        #run checks on prop data
        if not(self.checks_functionality.check_prop_data(prop_metadata_node)):

            #log
            self.logger.debug('Prop data check failed for node {0}. Check asset_name and namespace settings. Not exporting.'.format(prop_metadata_node.name()))
            return
        

        #proxy
        if(prop_metadata_node.proxy_export.get()):

            #export part
            self.export_part(shot_metadata_node, prop_metadata_node, 'helga_proxy', dry_run)


        #rendergeo
        if(prop_metadata_node.rendergeo_export.get()):

            #export part
            self.export_part(shot_metadata_node, prop_metadata_node, 'helga_rendergeo', dry_run)

        
        #locator
        if(prop_metadata_node.locator_export.get()):

            #export part
            self.export_part(shot_metadata_node, prop_metadata_node, 'helga_locator', dry_run)


    def export_char(self, 
                    shot_metadata_node, 
                    char_metadata_node, 
                    dry_run):
        """
        Export char for given char_metadata_node.
        Base data checks have passed at this point so its save to
        pass the shot_metadata_node and retrieve its values
        again.
        """

        #run checks on char data
        if not(self.checks_functionality.check_char_data(char_metadata_node)):

            #log
            self.logger.debug('Char data check failed for node {0}. Check asset_name and namespace settings. Not exporting.'.format(char_metadata_node.name()))
            return
        

        #proxy
        if(char_metadata_node.proxy_export.get()):

            #export part
            self.export_part(shot_metadata_node, char_metadata_node, 'helga_proxy', dry_run)


        #rendergeo
        if(char_metadata_node.rendergeo_export.get()):

            #export part
            self.export_part(shot_metadata_node, char_metadata_node, 'helga_rendergeo', dry_run)

        
        #locator
        if(char_metadata_node.locator_export.get()):

            #export part
            self.export_part(shot_metadata_node, char_metadata_node, 'helga_locator', dry_run)


    def export_part(self, 
                    shot_metadata_node,
                    prop_or_char_metadata_node,
                    attr_name,
                    dry_run):
        """
        Export process for a certain pynode and its attribute configuration.
        The attribute configuration consists of:

        1. The namespace of the PyNode
        2. The attr. which is searched for in the nodes belonging to the namespace.
        These two factors are needed to create the node export list.
        
        The next step is to create the abc_command.

        Then the abc command and some other things will be closured
        and added to the queue.

        When this function is called, all checks have been passed, so
        it is save to just grab the values and use them.
        """

        #node_type_name
        node_type_name = type(prop_or_char_metadata_node).__name__

        #node type specific assignments
        
        #Chars
        if (node_type_name == 'HelgaCharacterMetadata'):
            #asset_name, namespace
            asset_name, namespace = self.checks_functionality.check_char_data(prop_or_char_metadata_node)
            #alembic_subdir
            alembic_subdir = 'chars'
        
        #Props
        elif (node_type_name == 'HelgaPropMetadata'):
            #asset_name, namespace
            asset_name, namespace = self.checks_functionality.check_prop_data(prop_or_char_metadata_node)
            #alembic_subdir
            alembic_subdir = 'props'


        #part type specific assignments

        #proxy
        if (attr_name == 'helga_proxy'):
            asset_name_suffix = '_proxy'
        #rendergeo
        elif (attr_name == 'helga_rendergeo'):
            asset_name_suffix = '_rendergeo'
        #locator
        elif (attr_name == 'helga_locator'):
            asset_name_suffix = '_locator'

        
        
        #alembic_path, shot_start, shot_end
        alembic_path, shot_start, shot_end = self.checks_functionality.check_base_data(shot_metadata_node)

        #start frame offset enabled
        if (self.get_abc_start_frame_offset_enabled()):
            
            #shot_start + offset (Offset is negative by default)
            shot_start = shot_start + self.get_abc_start_frame_offset()
        

        #alembic_export_path
        alembic_export_path = alembic_path +'/' +alembic_subdir +'/' +asset_name +asset_name_suffix +'.abc'
        


        #node_export_list
        node_export_list = self.maya_functionality.get_nodes_with_namespace_and_attr(prop_or_char_metadata_node, attr_name)
        #check
        if not (node_export_list):
            #log
            self.logger.debug('Node export list for asset: {0} and part {1} empty. Not exporting part.'.format(asset_name, attr_name))
            return

        
        #abc_command
        abc_command = self.alembic_functionality.build_export_command(node_export_list, 
                                                                        [shot_start, shot_end], 
                                                                        alembic_export_path)

        
        #env_dict
        env_dict = self.get_env_dict(shot_metadata_node, prop_or_char_metadata_node, attr_name)
        #add abc_command
        env_dict.setdefault('HELGA_ABC_COMMAND', abc_command)

        
        #dry_run
        if(dry_run):

            #log
            self.logger.debug('{0}'.format(abc_command))
            
        #no dry_run
        else:
            
            #get closure and add to thread queue
            self.add_export_closure_to_queue(env_dict)

    
    def add_export_closure_to_queue(self, env_dict):
        """
        Create export closure from given abc_command and current maya_file and
        add export closure to thread queue.
        If the current maya file could not be retrieved (new file for example), 
        no closure will be added.
        """

        #export_thread_timeout
        export_thread_timeout = self.get_export_thread_timeout()

        #hide_export_shell
        hide_export_shell = self.get_hide_export_shell()

        #export_closure
        export_closure = self.alembic_functionality.get_export_closure(env_dict,
                                                                        export_thread_timeout,
                                                                        hide_export_shell)

        
        #progressbar range signal
        self.increment_progressbar_range()

        #add to queue
        self.threads_functionality.add_to_queue(export_closure)

        

        

    




    #Env. dict. methods
    #------------------------------------------------------------------ 

    def get_env_dict(self, 
                    shot_metadata_node,
                    prop_or_char_metadata_node = None,
                    attr_name = None):
        """
        Extend base_env_dict with custom attrs.
        At this point, all checks for the data have passed, so it is save to
        just retrieve the data without checking again.
        """

        #env_dict
        env_dict = os.environ.copy()

        #base_metadata_dict
        base_metadata_dict = self.get_base_metadata_dict(shot_metadata_node)
        env_dict.update(base_metadata_dict)

        
        #metadata_mode
        metadata_mode = self.get_metadata_mode()

        #Shot
        if (metadata_mode == 'shot'):

            #shot_metadata_dict
            shot_metadata_dict = self.get_shot_metadata_dict(shot_metadata_node)
            env_dict.update(shot_metadata_dict)


        #Prop
        elif (metadata_mode == 'prop'):

            #prop_metadata_dict
            prop_metadata_dict = self.get_prop_metadata_dict(shot_metadata_node, 
                                                                prop_or_char_metadata_node, 
                                                                attr_name)
            env_dict.update(prop_metadata_dict)

        
        #Char
        elif (metadata_mode == 'char'):

            #char_metadata_dict
            char_metadata_dict = self.get_char_metadata_dict(shot_metadata_node,
                                                                prop_or_char_metadata_node, 
                                                                attr_name)
            env_dict.update(char_metadata_dict)


        #return
        return env_dict

        
    def get_base_metadata_dict(self, shot_metadata_node):
        """
        Get dict with base data for export.
        """

        #base_metadata_dict
        base_metadata_dict = {}

        #metadata mode
        base_metadata_dict.setdefault('HELGA_ABC_METADATA_MODE', self.get_metadata_mode())

        #add maya_file_path
        base_metadata_dict.setdefault('HELGA_ABC_MAYA_FILE', str(self.maya_functionality.get_maya_file()))

        
        #alembic_path, shot_start, shot_end
        alembic_path, shot_start, shot_end = self.checks_functionality.check_base_data(shot_metadata_node)

        #add to base_metadata_dict
        base_metadata_dict.setdefault('HELGA_ABC_SHOT_START', str(shot_start))
        base_metadata_dict.setdefault('HELGA_ABC_SHOT_END', str(shot_end))
        base_metadata_dict.setdefault('HELGA_ABC_ALEMBIC_PATH', str(alembic_path))

        
        #abc_start_frame_offset_enabled
        abc_start_frame_offset_enabled = self.get_abc_start_frame_offset_enabled()
        #abc_start_frame_offset
        abc_start_frame_offset = self.get_abc_start_frame_offset()
        
        #add to base_metadata_dict
        base_metadata_dict.setdefault('HELGA_ABC_START_FRAME_OFFSET_ENABLED', str(abc_start_frame_offset_enabled))
        base_metadata_dict.setdefault('HELGA_ABC_START_FRAME_OFFSET', str(abc_start_frame_offset))
        
        
        

        #return
        return base_metadata_dict


    def get_shot_metadata_dict(self, shot_metadata_node):
        """
        Get dict with shot data for export.
        """

        #shot_metadata_dict
        shot_metadata_dict = {}


        #shot_cam
        shot_cam = self.checks_functionality.check_shot_data(shot_metadata_node)
        shot_metadata_dict.setdefault('HELGA_ABC_SHOT_CAM', str(shot_cam))


        #alembic_path, shot_start, shot_end
        alembic_path, shot_start, shot_end = self.checks_functionality.check_base_data(shot_metadata_node)
        
        
        #alembic_export_path
        alembic_subdir = 'cameras'
        asset_name = 'shot_cam'
        alembic_export_path = alembic_path +'/' +alembic_subdir +'/' +asset_name +'.abc'
        shot_metadata_dict.setdefault('HELGA_ABC_ALEMBIC_SUBDIR', alembic_subdir)
        shot_metadata_dict.setdefault('HELGA_ABC_ASSET_NAME', asset_name)
        shot_metadata_dict.setdefault('HELGA_ABC_ALEMBIC_EXPORT_PATH', str(alembic_export_path))

        
        #return
        return shot_metadata_dict


    def get_prop_metadata_dict(self, shot_metadata_node, prop_metadata_node, attr_name):
        """
        Get dict with prop data for export.
        """

        #alembic_path, shot_start, shot_end
        alembic_path, shot_start, shot_end = self.checks_functionality.check_base_data(shot_metadata_node)


        
        #prop_metadata_dict
        prop_metadata_dict = {}

        #asset_name, namespace
        asset_name, namespace = self.checks_functionality.check_prop_data(prop_metadata_node)
        prop_metadata_dict.setdefault('HELGA_ABC_NAMESPACE', str(namespace))
        

        #part type specific assignments

        #proxy
        if (attr_name == 'helga_proxy'):
            asset_name_suffix = '_proxy'
        #rendergeo
        elif (attr_name == 'helga_rendergeo'):
            asset_name_suffix = ''
        #locator
        elif (attr_name == 'helga_locator'):
            asset_name_suffix = '_locator'

        
        #alembic_subdir
        alembic_subdir = 'props'

        #alembic_export_path
        alembic_export_path = alembic_path +'/' +alembic_subdir +'/' +asset_name +asset_name_suffix +'.abc'
        prop_metadata_dict.setdefault('HELGA_ABC_ALEMBIC_SUBDIR', alembic_subdir)
        prop_metadata_dict.setdefault('HELGA_ABC_ASSET_NAME', str(asset_name))
        prop_metadata_dict.setdefault('HELGA_ABC_ASSET_NAME_SUFFIX', asset_name_suffix)
        prop_metadata_dict.setdefault('HELGA_ABC_ALEMBIC_EXPORT_PATH', str(alembic_export_path))

        
        #return
        return prop_metadata_dict


    def get_char_metadata_dict(self, shot_metadata_node, char_metadata_node, attr_name):
        """
        Get dict with char data for export.
        """

        #alembic_path, shot_start, shot_end
        alembic_path, shot_start, shot_end = self.checks_functionality.check_base_data(shot_metadata_node)

        

        #char_metadata_dict
        char_metadata_dict = {}

        #asset_name, namespace
        asset_name, namespace = self.checks_functionality.check_char_data(char_metadata_node)
        char_metadata_dict.setdefault('HELGA_ABC_NAMESPACE', str(namespace))
        

        #part type specific assignments

        #proxy
        if (attr_name == 'helga_proxy'):
            asset_name_suffix = '_proxy'
        #rendergeo
        elif (attr_name == 'helga_rendergeo'):
            asset_name_suffix = ''
        #locator
        elif (attr_name == 'helga_locator'):
            asset_name_suffix = '_locator'

        
        
        #alembic_subdir
        alembic_subdir = 'chars'
        
        #alembic_export_path
        alembic_export_path = alembic_path +'/' +alembic_subdir +'/' +asset_name +asset_name_suffix +'.abc'
        char_metadata_dict.setdefault('HELGA_ABC_ALEMBIC_SUBDIR', alembic_subdir)
        char_metadata_dict.setdefault('HELGA_ABC_ASSET_NAME', str(asset_name))
        char_metadata_dict.setdefault('HELGA_ABC_ASSET_NAME_SUFFIX', asset_name_suffix)
        char_metadata_dict.setdefault('HELGA_ABC_ALEMBIC_EXPORT_PATH', str(alembic_export_path))

        
        #return
        return char_metadata_dict

    






    



    #Test
    #------------------------------------------------------------------

    def dummy_method(self, msg = 'dummy'):
        """
        Dummy method
        """

        #log
        self.logger.debug('{0}'.format(msg))
        #print
        print('{0}'.format(msg))


    def stylesheet_test(self, wdgt):
        """
        Test if setting a stylesheet overrides all attributes or just
        the one it is setting.
        """

        #stylesheet_str
        stylesheet_str = 'background-color: red;'
        
        #set stylesheet
        wdgt.setStyleSheet(stylesheet_str)


    def progressbar_test_run(self, minimum, maximum, interval = 50):
        """
        Test the progressbar in action.
        """

        '''
        try:
            
            try:
                #stop timer
                self.progress_bar_test_timer.stop()
            except:
                pass

            #set range
            self.progressbar.setRange(minimum, maximum)
            #reset
            self.progressbar.setValue(minimum)

            #progress_bar_test_timer
            self.progress_bar_test_timer = QtCore.QTimer(self)
            self.progress_bar_test_timer.setObjectName('progress_bar_test_timer')
            self.progress_bar_test_timer.timeout.connect(self.increment_progressbar)
            self.progress_bar_test_timer.start(interval)

            #while
            while (True):

                if (self.progressbar.value() < maximum)
                
                QtGui.qApp.processEvents()

            #stop timer
            self.progress_bar_test_timer.stop()
        
        except:
            
            #log
            self.logger.debug('Error in progressbar test run. Maybe the object has been destroyed.')

        '''

        #log
        self.logger.debug('Currently disfunctional.')

        
        

    def test_methods(self):
        """
        Suite of test methods to execute on startup.
        """

        #log
        self.logger.debug('\n\nExecute test methods:\n-----------------------------')


        
        #test methods here
        #------------------------------------------------------------------

        #dummy_method
        self.dummy_method()

        #maya_functionality test
        print(self.maya_functionality.get_nodes_of_type('HelgaShotsMetadata'))

        #stylesheet_test
        #self.stylesheet_test(self.wdgt_explanation)

        #------------------------------------------------------------------



        #log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')


    








#Run
#------------------------------------------------------------------

def run(show_menu = True):
    """
    Standardized run() method
    """
    
    #asset_manager_instance
    asset_manager_instance = AssetManager(show_menu = show_menu)
    asset_manager_instance.show()










#Test setup home
#------------------------------------------------------------------

def run_home():
    """
    Copy and run @ home.
    Not to be used by anyone ever.
    """

    #Import
    #------------------------------------------------------------------
    #python
    import os
    import sys
    import shutil
    


    #Globals
    #------------------------------------------------------------------
    SOURCE_DIR = r'D:/filmaka/projects/helga/Production/scripts/work/helga/helga/maya/import_export'#dir to copy
    TARGET_DIR = r'D:/filmaka/projects/helga/Production/scripts/sandbox/helga/helga/maya/import_export'#source_dir is deleted from here if it exists and then copied in there

    

    #Delete existing
    #------------------------------------------------------------------
    try:
        if(os.path.isdir(TARGET_DIR)):
            print('Delete Dir: {0}'.format(TARGET_DIR))
            shutil.rmtree(TARGET_DIR)

    except:
        print('Error deleting Target Dir, maybe it doesnt exist. Not copying. - {0}'.format(TARGET_DIR))
        


    #Copy
    #------------------------------------------------------------------
    
    try:
        if(os.path.isdir(SOURCE_DIR)):
            print('Copy {0} to {1}'.format(SOURCE_DIR, TARGET_DIR))
            shutil.copytree(SOURCE_DIR, TARGET_DIR)
            
    
    except:
        print('Copying failed. Returning. {0} to {1}'.format(SOURCE_DIR, TARGET_DIR))
        return
    





    #Run
    #------------------------------------------------------------------
    #helga
    from helga.maya.import_export.asset_manager import asset_manager
    reload(asset_manager)
    
    #asset_manager_instance
    asset_manager_instance = asset_manager.AssetManager()
    asset_manager_instance.show()



#run_home()




#Test
#------------------------------------------------------------------

if (__name__ == '__main__'):

    #run
    run()