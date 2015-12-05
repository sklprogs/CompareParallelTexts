#!/usr/bin/python3

__author__ = 'Peter Sklyar'
__copyright__ = 'Copyright 2015, Peter Sklyar'
__license__ = 'GPL v.3'
__version__ = '1.0.1'
__email__ = 'skl.progs@gmail.com'

import os
import sys
import mes_ru
#import mes_en
import posixpath
import re
import codecs
from charade.universaldetector import UniversalDetector
from time import time
# Graphics
import tkinter as tk
import tkinter.messagebox as tkmes
import tkinter.filedialog as dialog
import eg_mod as eg

# Standalone code (1)
lev_crit='CRITICAL'
lev_err='ERROR'
lev_warn='WARNING'
lev_info='INFO'
lev_debug_err='DEBUG-ERROR'
lev_debug='DEBUG'

# Скрытые сообщения об ошибках
err_mes_unavail='CF_UNICODETEXT_UNAVAILABLE'
err_mes_copy='CLIPBOARD_COPY_ERROR'
err_mes_paste='CLIPBOARD_PASTE_ERROR'
err_wrong_enc='WRONG_ENCODING_ERROR'
err_incor_log_mes='INCORRECT_LOG_MESSAGE'
cur_widget='ERR_NO_WIDGET_DEFINED'
err_mes_no_feature_text='ERR_NO_FEATURE_TEXT'
err_mes_no_full_inq_text='ERR_NO_FULL_INQ_TEXT'
err_mes_no_inq_path='ERR_NO_INQ_PATH'
err_mes_empty_question='ERR_EMPTY_QUESTION'
err_mes_empty_warning='ERR_EMPTY_WARNING'
err_mes_empty_info='ERR_EMPTY_INFO'
err_mes_empty_error='ERR_EMPTY_ERROR'
err_mes_empty_input='ERR_EMPTY_INPUT'
err_mes_no_selection='ERR_NO_SELECTION'
err_mes_selected_not_matched='SELECTED_NOT_MATCHED'
err_mes_empty_mes='EMPTY_MESSAGE'
err_mes_unsupported_lang='ERR_UNSUPPORTED_LANGUAGE'
cmd_err_mess=[err_mes_unavail,err_mes_copy,err_mes_paste,err_wrong_enc,err_incor_log_mes,err_mes_no_feature_text,err_mes_no_full_inq_text,err_mes_no_inq_path,err_mes_empty_question,err_mes_empty_warning,err_mes_empty_info,err_mes_empty_error,err_mes_empty_input,err_mes_no_selection,err_mes_selected_not_matched,err_mes_empty_mes,err_mes_unsupported_lang]

ru_alphabet='№АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщыъьэюя'
lat_alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
figures='0123456789'
punctuation='.,;:!?'
other_symbols='"@#$%^&*()[]{}\/|  +=-–—_<>	«“”»'+"'’"
allowed_syms=['°']

default_encoding = "utf-8"
BOM = '\N{ZERO WIDTH NO-BREAK SPACE}'
dlb = "\n"
wdlb = '\r\n'
tab = '        '

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# shared code
# В этой функции лог еще не подключен, поэтому отмена всех операций не поддерживается
# Проверить существование файла
def exist(cur_file,Silent=False,Critical=True):
	cur_func = sys._getframe().f_code.co_name
	if os.path.exists(cur_file):
		Success=True
	else:
		Success=False
		mestype(cur_func,globs['mes'].file_not_found % cur_file,Silent=Silent,Critical=Critical)
	# Лог еще не подключен
	return Success
	
# Показать сообщение определенного типа в зависимости от параметров
def mestype(func,cur_mes,Silent=False,Critical=False,Info=False):
	if Critical and not Info:
		ErrorMessage(func,cur_mes)
	else:
		if Info:
			if Silent:
				log(func,lev_info,cur_mes)
			else:
				InfoMessage(func,cur_mes)
		else:
			if Silent:
				log(func,lev_warn,cur_mes)
			else:
				Warning(func,cur_mes)
				
# Названия такие же, как у модуля PyZenity (кроме List)
# Информация
def InfoMessage(cur_func='MAIN',cur_mes=''):
	root.withdraw()
	tkmes.showinfo(globs['mes'].inf_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_info,cur_mes)
	
# Предупреждение
def Warning(cur_func='MAIN',cur_mes=''):
	root.withdraw()
	tkmes.showwarning(globs['mes'].warn_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_warn,cur_mes)
	
# Placeholders
def log(cur_func,level,log_mes,TransFunc=False):
	#print(cur_func,':',level,':',log_mes)
	pass

def decline_nom(words_nf,Decline=False):
	pass

def check_args(func,arg_list):
	pass

def check_type(*args):
	pass

# Ошибка
def ErrorMessage(cur_func='MAIN',cur_mes='',Critical=True):
	root.withdraw()
	tkmes.showerror(globs['mes'].err_head,cur_mes)
	if Critical:
		log(cur_func,lev_crit,cur_mes)
		sys.exit()
	else:
		log(cur_func,lev_err,cur_mes)
	root.deiconify()
	
# Диалог открытия файла с различными параметрами
# При PersistPar диалог открывается в $HOME, даже если напрямую указать файл!
def dialog_open_file(dir,my_title=None,mask='*',PersistPar=False,Critical=True):
	cur_func=sys._getframe().f_code.co_name
	file=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if empty(my_title):
			my_title=globs['mes'].select_file
		# ВНИМАНИЕ: параметры меняются в зависимости от версии easygui
		# Допустимые на данный момент параметры (их также необходимо указывать): msg, title, default, filetypes
		# Параметр default передает easygui имя файла. Если передать каталог, то последний каталог будет проигнорирован, поэтому вставляем sysdiv. Сразу default передать не получается, поэтому предварительно создаем переменную dir.
		# mask появляется только во всплывающем списке после 'All Files'
		if dir[-1] == sysdiv:
			dir=dir[:-1]
		exist(dir)
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if len(mask) > 0:
				if mask=='*':
					dir=dir+sysdiv+'*'
				elif mask[0]=='*':
					dir=dir+sysdiv+mask
				else:
					dir=dir+sysdiv+'*'+mask
			else:
				dir=dir+sysdiv+'*'
			# При PersistPar диалог открывается в $HOME, даже если напрямую указать файл!
			root.withdraw()
			try:
				file=eg.fileopenbox(title=my_title,default=dir,filetypes=mask)
			except:
				mestype(cur_func,globs['mes'].file_sel_failed,Critical=Critical)
			if empty(file) and Critical:
				sys.exit()
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if PersistPar:
					if empty(file):
						globs['AbortAll']=True
				root.deiconify()
	log(cur_func,lev_debug,str(file))
	# Возвращает абсолютный путь
	return file

# Удостовериться, что входная строка имеет какую-то ценность
def empty(my_input):
	cur_func=sys._getframe().f_code.co_name
	par=True # При отмене всех задач должно возвращаться True, иначе 'if not empty()' в таких случаях возвращает True!
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if my_input=='' or my_input==None or my_input==[] or my_input==() or my_input=={} or my_input in cmd_err_mess:
			par=True
		else:
			par=False
		log(cur_func,lev_debug,str(par))
	return par

# Верно определить каталог по полному пути вне зависимости от ОС
def true_dirname(path,UseLog=True):
	cur_func=sys._getframe().f_code.co_name
	curdir=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		path=path.replace('\\','//')
		#curdir=ntpath.dirname(path)
		curdir=posixpath.dirname(path)
		if sys_type=='win':
			curdir=curdir.replace('//','\\')
		if UseLog:
			log(cur_func,lev_debug,globs['mes'].full_path2 % (path,curdir))
	return curdir
	
# В этой функции лог еще не подключен, поэтому отмена всех операций не поддерживается
# Определить тип ОС
def detect_os():
	#cur_func=sys._getframe().f_code.co_name
	if 'win' in sys.platform:
		par='win'
	elif 'lin' in sys.platform:
		par='lin'
	elif 'mac' in sys.platform:
		par='mac'
	else:
		par='unknown'
	# Занесение в лог здесь делать рано, конфиг еще не прочитан
	#log(cur_func,lev_debug,str(par))
	return par
	
# Remove a tag within a range
def tag_remove(widget,tag_name,pos1tk='1.0',pos2tk='end',Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			widget.tag_remove(tag_name,pos1tk,pos2tk)
			log(cur_func,lev_debug,globs['mes'].tag_removed % (tag_name,pos1tk,pos2tk))
		except tk.TclError:
			mestype(cur_func,globs['mes'].tag_remove_failed % (tag_name,str(widget),pos1tk,pos2tk),Silent=Silent,Critical=Critical)
			
# Add a mark
def mark_add(widget,mark_name,postk,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	check_args(cur_func,[[mark_name,globs['mes'].type_str],[postk,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			widget.mark_set(mark_name,postk)
			log(cur_func,lev_debug,globs['mes'].mark_added % (mark_name,postk))
		except tk.TclError:
			mestype(cur_func,globs['mes'].mark_addition_failure % (mark_name,postk),Silent=Silent,Critical=Critical)
			
# Remove a mark
def mark_remove(widget,mark_name,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	check_args(cur_func,[[mark_name,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			widget.mark_unset(mark_name)
			log(cur_func,lev_debug,globs['mes'].mark_removed % (mark_name))
		except tk.TclError:
			mestype(cur_func,globs['mes'].mark_removal_failure % mark_name,Silent=Silent,Critical=Critical)

# Add and configure a tag
def tag_add_config(widget,tag_name,pos1tk,pos2tk,mode='bg',color='cyan'):
	cur_func = sys._getframe().f_code.co_name
	check_args(cur_func,[[tag_name,globs['mes'].type_str],[pos1tk,globs['mes'].type_str],[pos2tk,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# 1. Установка тэга
		try:
			widget.tag_add(tag_name,pos1tk,pos2tk)
			log(cur_func,lev_debug,globs['mes'].tag_added % (tag_name,pos1tk,pos2tk))
		except:
			log(cur_func,lev_err,globs['mes'].tag_addition_failure % (tag_name,pos1tk,pos2tk))	
		# 2. Настройка тэга
		try:
			if mode == 'bg':
				widget.tag_config(tag_name,background=color)
				log(cur_func,lev_debug,globs['mes'].tag_bg % (tag_name,color))
			elif mode == 'fg':
				widget.tag_config(tag_name,foreground=color)
				log(cur_func,lev_debug,globs['mes'].tag_fg % (tag_name,color))
			else:
				ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'bg, fg'))
		except:
			if mode == 'fg':
				log(cur_func,lev_err,globs['mes'].tag_fg_failure % tag_name)
			else:
				log(cur_func,lev_err,globs['mes'].tag_bg_failure % tag_name)

# Get a current cursor position
def get_cursor(widget,pane_no=1):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		pos = '1.0'
		try:
			pos = widget.index('sel.last')
			# In case of no selection tkinter will raise an error, so we return a position of the cursor
		except:
			try:
				pos = widget.index('insert')
			except:
				log(cur_func,lev_warn,globs['mes'].no_selection2 % pane_no)
	return pos
	
# Make a tag visible
def drag_screen(widget,mark,pane_no=1):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			widget.yview(mark)
		except:
			log(cur_func,lev_err,globs['mes'].shift_screen_failure2 % (pane_no,mark))

# Get a word number by a position of its symbol
def get_word_by_pos(text_db,pos):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if not 'word_no' in text_db:
			text_db['word_no'] = 0
		for i in range(text_db['words_num']):
			# Include a space after a word (+1)
			if pos >= text_db['first_syms'][i] and pos <= text_db['last_syms'][i]+1:
				text_db['word_no'] = i
				break
				
# Определить язык текста (lat, ru, mixed, none)
def langdet(text):
	cur_func=sys._getframe().f_code.co_name
	par='lat'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		cyr_par=False
		lat_par=False
		for i in range(len(ru_alphabet)):
			if ru_alphabet[i] in text:
				cyr_par=True
				break
		for i in range(len(lat_alphabet)):
			if lat_alphabet[i] in text:
				lat_par=True
				break
		if cyr_par and lat_par:
			par='mixed'
		elif cyr_par:
			par='ru'
		elif lat_par:
			par='lat'
		else:
			par='none'
		log(cur_func,lev_debug,str(par))
	return par

# Определить, из каких символов состоит текст (lat, ru, mixed)
# Отличие от простого langdet в том, что один и тот же текст может включать буквы разных алфавитов, а нам надо вычислить, букв каких алфавитов больше
def langdet_profound(line,Verbose=False,Strict=False):
	cur_func = sys._getframe().f_code.co_name
	par = 'lat'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		par = 'mixed'
		orig_line = line
		line = line.lower()
		line = list(line)
		ru_count = 0
		lat_count = 0
		fig_count = 0
		punc_count = 0
		other_count = 0
		for i in range(len(line)):
			if line[i] in ru_alphabet:
				ru_count += 1
			elif line[i] in lat_alphabet:
				lat_count += 1
			elif line[i] in figures:
				fig_count += 1
			elif line[i] in punctuation:
				punc_count += 1
			else:
				if Strict:
					if not line[i] in other_symbols:
						other_count += 1
				else:
					other_count += 1
		if Verbose:
			InfoMessage(cur_func,globs['mes'].verbose_stat % (orig_line,lat_count,ru_count,fig_count,punc_count,other_count))
		array = [ru_count,lat_count,fig_count,punc_count,other_count]
		array.sort(reverse=True)
		if Strict:
			if ru_count > 0:
				par = 'ru'
			elif other_count > 0:
				par = 'mixed'
			else:
				par = 'lat'
		else:
			if array[0] == array[1]:
				par = 'mixed'
			elif array[0] == lat_count:
				par = 'lat'
			elif array[0] == ru_count:
				par = 'ru'
		if Verbose:
			cur_mes = globs['mes'].stat_pattern1
			cur_mes_add = ''
			if par == 'lat':
				cur_mes_add = globs['mes'].stat_pattern2
			elif par == 'ru':
				cur_mes_add = globs['mes'].stat_pattern3
			else:
				cur_mes = globs['mes'].diverse_text
			cur_mes += cur_mes_add
			InfoMessage(cur_func,cur_mes)
		log(cur_func,lev_debug,str(par))
	return par
	
# Find a number which is closest to the given number in the given list of numbers. Only the first instance is supported. Integer/float values are supported.
def get_closest(num_lst,num):
	cur_func = sys._getframe().f_code.co_name
	word_no = 0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Lists in Python go beyond functions, so we create a new instance that can be safely modified
		test_lst = list(num_lst)
		for i in range(len(test_lst)):
			test_lst[i] = abs(test_lst[i] - num)
		word_no = test_lst.index(min(test_lst))
	return word_no
	
# Find word(s) in text widget(s)
def search_pane(text_db,widget,direction='forward',pane_no=1): # clear, forward, backward
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if direction == 'clear': # Search again
			if 'search_list' in text_db:
				del text_db['search_list']
			direction = 'forward'
		elif direction != 'forward' and direction != 'backward':
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(direction),'clear, forward, backward'))
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			# Preserving initial values
			if not 'search_list' in text_db:
				search_str = text_field(title=globs['mes'].search_str,Small=True) #search_field.get()
				search_str = search_str.strip(' ').strip(dlb)
				search_str = search_str.lower()
				root.withdraw()
				if not empty(search_str):
				# Create a list of positions of all search matches 
					text_db['search_list'] = []
					i=0
					while i < text_db['words_num']:
						# A less strict search - 'words_nf' (in that case, .lower() is not required)
						if search_str in text_db['words'][i].lower():
							text_db['search_list'].append(i)
						i += 1
					text_db['len_search_list'] = len(text_db['search_list'])
					if text_db['len_search_list'] > 0:
						if direction == 'forward':
							# A number of a current search result ('search_elem_no') in the list of search matches ('search_list')
							text_db['search_elem_no'] = -1
						elif direction == 'backward':
							text_db['search_elem_no'] = text_db['len_search_list']
			if 'search_list' in text_db and 'len_search_list' in text_db:
				# Continue the search from the previous position
				if text_db['len_search_list'] > 0:
					if direction == 'forward':
						if text_db['search_elem_no'] + 1 < text_db['len_search_list']:
							text_db['search_elem_no'] += 1
						else:
							text_db['search_elem_no'] = 0
					elif direction == 'backward':
						if text_db['search_elem_no'] > 0:
							text_db['search_elem_no'] -= 1
						else:
							text_db['search_elem_no'] = text_db['len_search_list'] - 1
					if len(text_db['search_list']) > 0:
						word_no = text_db['search_list'][text_db['search_elem_no']]
						pos1 = text_db['first_syms'][word_no]
						pos2 = text_db['last_syms'][word_no]
						lift_pos = pos1
						pos1 = pos2tk(text_db,pos1,Even=False)
						pos2 = pos2tk(text_db,pos2,Even=True)
						tag_remove(widget,'search','1.0','end')
						mark_remove(widget,'insert',Silent=True)
						if globs['bool']['UseHeadInterval']:
							# Experimentally supported values
							if lift_pos - 1000 >= 0:
								lift_pos -= 1000
						lift_pos = pos2tk(text_db,lift_pos,Even=False)
						mark_add(widget,'insert',lift_pos)
						tag_add_config(widget,'search',pos1,pos2,color='gray')
						drag_screen(widget,'insert',pane_no=pane_no)
						
# Конструктор для создания окна для манипуляции текстом
def text_field(title=None,user_text=err_mes_empty_input,CheckSpelling=False,GoTo='',Insist=False,SelectAll=False,ReadOnly=False,Small=False,TrimEnd=False): # Edit=True равноценно user_text!=err_mes_empty_input
	cur_func=sys._getframe().f_code.co_name
	func_res=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Если правописание (globs['bool']['Spelling']) отключено в конфиге, то отключить и опциональный параметр CheckSpelling
		if not globs['bool']['Spelling']:
			CheckSpelling=False
		top, res = tk.Toplevel(root), [None]
		if globs['bool']['AlwaysMaximize'] and not Small:
			if sys_type=='lin':
				top.wm_attributes('-zoomed',True)
			# Win, Mac
			else:
				top.wm_state(newstate='zoomed')
		def close_top(event):
			top.destroy()
			root.deiconify()
		def callback(event):
			if Small:
				returned=widget.get()
			elif ReadOnly:
				returned=user_text
			else:
				returned=widget.get(1.0,'end')
			# На входе без ошибок (пока) принимаются список и строка
			if get_obj_type(returned,Verbal=True)==globs['mes'].type_str:
				returned=returned.strip(dlb)
			res[0]=returned
			close_top(None)
		root.withdraw()
		if empty(title):
			title=globs['mes'].text
		title+=' '+my_program_title
		top.title(title)
		#top.tk.call('wm','iconphoto',top._w,tk.PhotoImage(file=globs['var']['icon_main']))
		# Позволяет удалять пробел и пунктуацию с конца, что полезно при некорректной обработке Ctrl+Shift+->
		if TrimEnd and not Small: # По текущим данным, globs['bool']['UnixSelection'] не работает с Entry
			user_text=delete_end_punc(user_text)
		if Small:
			widget=tk.Entry(top,font=globs['var']['font_style'])
		else:
			scrollbar=tk.Scrollbar(top,jump=0)
			widget=tk.Text(top,height=10,font=globs['var']['font_style'],wrap='word',yscrollcommand=scrollbar.set)
		if not empty(user_text):
			widget.insert('end',user_text)
		if ReadOnly and globs['bool']['ReadOnlyProtection'] and not Small:
			widget.config(state='disabled')
		if not Small:
			# Позволяет использовать мышь для управления скроллбаром
			scrollbar.config(command=widget.yview)
			scrollbar.pack(side='right',fill='y')
		create_binding(widget=widget,bindings=['<Return>','<KP_Enter>'],action=callback)
		if CheckSpelling:
			text_db=analyse_text(user_text,Truncate=False,Decline=False)
			misspel_lst=check_spelling(text_db)
			misspel_lst=list2tk(misspel_lst)
			for i in range(len(misspel_lst)):
				pos1=misspel_lst[i][0]
				pos2=misspel_lst[i][1]
				try:
					widget.tag_add('missp',pos1,pos2)
					log(cur_func,lev_debug,globs['mes'].tag_added % ('missp',pos1,pos2))
				except:
					log(cur_func,lev_err,globs['mes'].tag_addition_failure % ('missp',pos1,pos2))
			try:
				widget.tag_config('missp',background='red')
				log(cur_func,lev_debug,globs['mes'].tag_bg % ('missp','red'))
			except:
				log(cur_func,lev_err,globs['mes'].tag_bg_failure % 'missp')
		if Small:
			widget.pack()
		else:
			widget.pack(expand=1,fill='both')
		# Выход по клику кнопки
		if ReadOnly:
			create_button(parent_widget=top,text=globs['mes'].btn_x,hint=globs['mes'].btn_x,action=callback,expand=1)
		else:
			create_button(parent_widget=top,text=globs['mes'].save_and_close,hint=globs['mes'].save_and_close,action=callback,expand=1)
		# Выход по нажатию Enter и Пробел на кнопке (навигация по Shift+Tab)
		widget.focus_force()
		if GoTo!='' and not Small:
			try:
				goto_pos=widget.search(GoTo,'1.0','end')
				widget.mark_set('goto',goto_pos)
				widget.mark_set('insert',goto_pos)
				widget.yview('goto')
			except:
				log(cur_func,lev_err,globs['mes'].shift_screen_failure % 'goto')
		else:
			try:
				widget.mark_set('insert','1.0')
			except:
				log(cur_func,lev_err,globs['mes'].cursor_insert_failure)
		if SelectAll:
			select_all(widget,Small=False)
		elif Small and not ReadOnly:
			select_all(widget,Small=True)
		create_binding(widget=widget,bindings='<Control-a>',action=lambda x:select_all(widget,Small=Small))
		globs['cur_widget']=widget
		if globs['bool']['UnixSelection'] and not Small: # По текущим данным, globs['bool']['UnixSelection'] не работает с Entry
			create_binding(widget=globs['cur_widget'],bindings='<Control-Shift-Left>',action=lambda x: top.after(20, left_sel_mod))
			create_binding(widget=globs['cur_widget'],bindings='<Control-Shift-Right>',action=lambda x: top.after(20, right_sel_mod))
		if Small or ReadOnly:
			create_binding(widget=widget,bindings='<Escape>',action=close_top)
		top.wait_window(top)
		func_res=res[0]
		log(cur_func,lev_debug,str(func_res))
		if Insist:
			if empty(func_res):
				ErrorMessage(cur_func,globs['mes'].empty_text)
			# Предотвратить возможные ошибки при глобальной отмене
		if func_res==None:
			func_res=''
	return func_res
	
# Конвертировать числовую позицию формата int в позицию в формате Tkinter
# Пример: 20 => '1.20'
def pos2tk(text_db,pos,Even=False):
	cur_func=sys._getframe().f_code.co_name
	tk_pos='1.0'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# < при len=maxi+1 и <= при len=maxi
		assert(pos < text_db['len'])
		#elem=text_db['pos_sl'][pos-1]
		# 2014-11-15 11:52
		elem=text_db['pos_sl'][pos]
		tk_pos=convert2tk(elem[0],elem[1],Even=Even)
		log(cur_func,lev_debug,str('%d => %s' % (pos,tk_pos)))
	return tk_pos
	
# Привести в вид, понимаемый виджетом Tk, список вида [sent_no,pos1]
def convert2tk(sent,pos,Even=False):
	cur_func=sys._getframe().f_code.co_name
	tk_str='1.0'
	check_args(cur_func,[[sent,globs['mes'].type_int],[pos,globs['mes'].type_int],[Even,globs['mes'].type_bool]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if Even:
			tk_str=str(sent+1)+'.'+str(pos+1)
		else:
			tk_str=str(sent+1)+'.'+str(pos)
		log(cur_func,lev_debug,str(tk_str))
	return tk_str
			
# Конвертировать позицию в формате Tkinter в числовую позицию формата int
# Пример: '1.20' => 20
def tk2pos(text_db,tk_pos,Even=False):
	cur_func=sys._getframe().f_code.co_name
	found=0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Пример: [0,10]
		pos_sl_no=convertFromTk(tk_pos,Even=Even)
		# Выделение в Tkinter может выйти за пределы самого текста, поэтому заранее определяем правую границу.
		found=len(text_db['pos_sl'])
		for i in range(len(text_db['pos_sl'])):
			if pos_sl_no==text_db['pos_sl'][i]:
				found=i
				break
		log(cur_func,lev_debug,str('%s => %s' % (tk_pos,str(found))))
	return found
	
# Конвертировать строку с позицией Tkinter вида '1.20' в список вида [sent_no,pos_no]
def convertFromTk(line,Even=False):
	cur_func=sys._getframe().f_code.co_name
	lst=[0,0]
	check_args(cur_func,[[line,globs['mes'].type_str],[Even,globs['mes'].type_bool]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		num_lst=line.split('.')
		assert(len(num_lst)==2)
		sent=str2int(num_lst[0])
		check_type(cur_func,sent,globs['mes'].type_int)
		pos=str2int(num_lst[1])
		check_type(cur_func,pos,globs['mes'].type_int)
		if Even:
			lst=[sent-1,pos-1]
		else:
			lst=[sent-1,pos]
		# Tkinter позволяет выделять так, что конец придется на первый (=нулевой) символ в начале предложения, и из-за Even получится отрицательное число. Компенсируем это.
		for i in range(len(lst)):
			if lst[i] < 0:
				log(cur_func,lev_warn,globs['mes'].negative % lst[i])
				lst[i]=0
		log(cur_func,lev_debug,str(lst))
	return lst
	
# Конвертировать строку в целое число
def str2int(line):
	cur_func=sys._getframe().f_code.co_name
	par=0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			par=int(line)
		except:
			log(cur_func,lev_err,globs['mes'].convert_to_int_failure % line)
		log(cur_func,lev_debug,str(par))
	return par
	
# Привязать горячие клавиши или кнопки мыши к действию
def create_binding(widget,bindings,action): # widget, list, function
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		bindings_type=get_obj_type(bindings,Verbal=True,IgnoreErrors=True)
		if bindings_type==globs['mes'].type_str or bindings_type==globs['mes'].type_lst:
			if bindings_type==globs['mes'].type_str:
				bindings=[bindings]
			for i in range(len(bindings)):
				try:
					widget.bind(bindings[i],action)
				except tk.TclError:
					Warning(cur_func,globs['mes'].wrong_keybinding % bindings[i])
		else:
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(bindings_type),'%s, %s' % (globs['mes'].type_str,globs['mes'].type_lst)))
			
# Вернуть тип параметра
def get_obj_type(obj,Verbal=True,IgnoreErrors=False):
	cur_func=sys._getframe().f_code.co_name
	obj_type_str=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		obj_type_str=str(type(obj))
		obj_type_str=obj_type_str.replace("<class '",'')
		obj_type_str=obj_type_str.replace("'>",'')
		# int, float, str, list, dict, tuple, NoneType
		if Verbal:
			obj_type_str=obj_type_verbal(obj_type_str,IgnoreErrors=IgnoreErrors)
		#log(cur_func,lev_debug,obj_type_str)
	return obj_type_str

# Название типа на русском
def obj_type_verbal(obj_type_str,IgnoreErrors=False):
	cur_func=sys._getframe().f_code.co_name
	obj_type_str=str(obj_type_str)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if obj_type_str=='str':
			obj_type_str=globs['mes'].type_str
		elif obj_type_str=='list':
			obj_type_str=globs['mes'].type_lst
		elif obj_type_str=='dict':
			obj_type_str=globs['mes'].type_dic
		elif obj_type_str=='tuple':
			obj_type_str=globs['mes'].type_tuple
		elif obj_type_str=='set' or obj_type_str=='frozenset':
			obj_type_str=globs['mes'].type_set
		elif obj_type_str=='int':
			obj_type_str=globs['mes'].type_int
		elif obj_type_str=='long':
			obj_type=globs['mes'].type_long_int
		elif obj_type_str=='float':
			obj_type_str=globs['mes'].type_float
		elif obj_type_str=='complex':
			obj_type_str=globs['mes'].type_complex
		elif obj_type_str=='bool':
			obj_type_str=globs['mes'].type_bool
		elif IgnoreErrors:
			pass
		else:
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (obj_type_str,'str, list, dict, tuple, set, frozenset, int, long, float, complex, bool'))
		#log(cur_func,lev_debug,obj_type_str)
	return obj_type_str
	
# Загрузить файл без разбиения на строки и вернуть как переменную
def load_file(file,List=False):
	cur_func=sys._getframe().f_code.co_name
	line=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		log(cur_func,lev_info,globs['mes'].loading_file % file)
		try:
			with open(file,'r',encoding=default_encoding) as f:
				line=f.read()
			log(cur_func,lev_info,globs['mes'].encoding_check_not_required % file)
		except:
			log(cur_func,lev_info,globs['mes'].encoding_check % file)
			reencode(file)
			delete_bom(file)
			convert_line_break(file)
			try:
				with open(file,'r',encoding=default_encoding) as f:
					line=f.read()
			except:
				# Лучше ErrorMessage, чем Warning, потому что на этапе tr_file_claims произойдет перезапись файла, даже если он не текстовый!
				ErrorMessage(cur_func,globs['mes'].file_read_failure % file)
		# Такой подробный лог не нужен
		#log(cur_func,lev_debug,str(line))
	if List:
		line = line.splitlines()
	return line
	
# Изменить кодировку файла на принятую по умолчанию (если требуется)
# Является частью load_file()
def reencode(file):
	cur_func=sys._getframe().f_code.co_name
	exist(file)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		source_encoding=detect_encoding(file)
		source_encoding=re.sub(".*]: ",'',source_encoding)
		source_encoding=re.sub(" с вероятностью .*",'',source_encoding)
		if source_encoding == default_encoding:
			log(cur_func,lev_info,globs['mes'].reencoding_not_required % file)
		else:
			convert_file(file,source_encoding,default_encoding)
			log(cur_func,lev_info,globs['mes'].reencoded % (file,default_encoding))
			
# Является частью load_file()
def detect_encoding(path):
	cur_func=sys._getframe().f_code.co_name
	func_res='unknown'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		"""Return a string describing the probable encoding of a file."""
		u = UniversalDetector()
		for line in open(path, 'rb'):
			u.feed(line)
		u.close()
		result = u.result
		if result['encoding']:
			func_res='[%s]: %s с вероятностью %s' % (path,result['encoding'],result['confidence'])
		log(cur_func,lev_debug,str(func_res))
	return func_res
	
# Изменить кодировку текстового файла
# Является частью load_file()
def convert_file(file_w,source_encoding,target_encoding):
	cur_func=sys._getframe().f_code.co_name
	Success=False
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success=True
		try:
			# Из-за бага в codecs.open() не удается сразу же открыть файл с помощью open() и возникают символы ďťż в начале текста
			a = codecs.open(file_w,"r",source_encoding).read()
			codecs.open(file_w,"w",target_encoding).write(a)
			log(cur_func,lev_info,globs['mes'].file_encoding_changed % file_w)
		except:
			Success=False
			Warning(cur_func,globs['mes'].file_encoding_failure % file_w)
		log(cur_func,lev_debug,str(Success))
	return Success
	
# Удалить отметку BOM
# Является частью load_file()
def delete_bom(file):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if globs['bool']['DeleteBOM']:
			log(cur_func,lev_info,globs['mes'].file_checking % str(file))
			# delete_bom теперь встроен в load_file, поэтому избегаем здесь рекурсии
			try:
				with open(file,'r',encoding=default_encoding) as f:
					text=f.read()
			except:
				ErrorMessage(cur_func,globs['mes'].file_read_failure % file)
			if BOM in text:
				log(cur_func,lev_info,globs['mes'].bom_found)
				text=text.replace(BOM,'')
				with open(file,'w',encoding=default_encoding) as f:
					f.write(text)
				log(cur_func,lev_info,globs['mes'].bom_deleted)
			else:
				log(cur_func,lev_info,globs['mes'].bom_not_found)
				
# Изменить тип переноса строки на тот, который задан по умолчанию
# Является частью load_file()
def convert_line_break(file):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		parts=detect_line_break(file)
		line_break=parts['line_break']
		line_break_os=parts['line_break_os']
		log(cur_func,lev_info,globs['mes'].old_line_break % (file,line_break_os))
		if not line_break_os==dlb_os:
			replace(file,line_break,dlb)
		parts=detect_line_break(file)
		line_break_os=parts['line_break_os']
		log(cur_func,lev_info,globs['mes'].new_line_break % (file,line_break_os))
		
# Определить тип переноса строки и соответствующую ОС
# "\r\n" (Windows), "\n" (Unix), "\r" (old Mac OS)
# Является частью load_file()
def detect_line_break(file):
	cur_func=sys._getframe().f_code.co_name
	func_res={'line_break':'\n','line_break_os':'unknown'}
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Встроено в load_file, поэтому избегаем рекурсии
		with open(file,'U',encoding=default_encoding) as f:
			f.readline()
			line_break=repr(f.newlines)
		# Перенос возвращается почему-то не в виде [\n], а в виде ['\n']
		line_break=line_break[1:len(line_break)-1]
		if line_break=="\\n":
			line_break_os='UNIX'
		elif line_break=="\\r\\n":
			line_break_os='Windows'
		elif line_break=="\\r":
			line_break_os='Old MacOS'
		else:
			line_break_os='unknown'
		func_res={'line_break':line_break,'line_break_os':line_break_os}
		log(cur_func,lev_debug,str(func_res))
	return func_res
	
# Заменить одну подстроку на другую в файле
# Является частью load_file()
def replace(file,replace_what,replace_with):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			with open(file,encoding=default_encoding) as f:
				text=f.read()
		except:
			ErrorMessage(cur_func,globs['mes'].file_read_failure % file)
		text=text.replace(replace_what,replace_with)
		# Critical=True было раньше. Оставляю для совместимости.
		write_file(file,text,mode='w',Critical=True,AskRewrite=False)
		
# Записать текст в файл в режиме 'write' или 'append'
# Critical распространяется только на попытку записи файла. Проверка режима обязана быть Critical
def write_file(file,text,mode='w',Silent=False,Critical=False,AskRewrite=False):
	cur_func=sys._getframe().f_code.co_name
	Success=False
	check_type(cur_func,file,globs['mes'].type_str)
	check_type(cur_func,mode,globs['mes'].type_str)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success=True
		if mode!='w' and mode!='a':
			Success=False
			mestype(cur_func,globs['mes'].wrong_mode % mode,Silent=False,Critical=True)
		if Success:
			try:
				with open(file,mode,encoding=default_encoding) as f:
					f.write(text)
				log(cur_func,lev_info,globs['mes'].file_written % file)
			except:
				Success=False
				mestype(cur_func,globs['mes'].file_write_failure % file,Silent=Silent,Critical=Critical)
		log(cur_func,lev_debug,str(Success))
	return Success
	
# Проанализировать текст и вернуть информацию о нем
def analyse_text(text,Truncate=True,Decline=False):
	cur_func=sys._getframe().f_code.co_name
	text_db={}
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		start_time=time()
		check_args(cur_func,[[text,globs['mes'].type_str],[Truncate,globs['mes'].type_bool]])
		# Нотация: lst = general list, clst = char list, wlst = word list, slst = sentence list
		first_syms=[] # позиции первых букв слов
		first_syms_sl=[] # позиции первых букв слов (отсчет от начала текущей строки)
		first_syms_nf=[]
		first_syms_nf_sl=[]
		words=[] # список слов
		# Для dlbs и nls делать _sl бессмысленно
		dlbs=[] # позиции dlb
		nls=[] # номера слов, с которых начинается новая строка
		spaces=[] # позиции пробелов
		spaces_sl=[] # позиции пробелов (отсчет от начала текущей строки)
		last_syms=[] # позиции последних букв слов
		last_syms_sl=[] # позиции последних букв слов (отсчет от начала текущей строки)
		last_syms_nf=[] # позиции последних букв слов без пунктуации
		last_syms_nf_sl=[] # позиции последних букв слов без пунктуации (отсчет от начала текущей строки)
		sent_nos=[] # список номеров строк для каждого слова
		words_nf=[] # список слов без пунктуации
		sents_sym_len=[] # Длина предложений в символах
		sents_word_len=[] # Список количеств слов в предложениях
		sents_text=[] # Список предложений с сохранением лишних пробелов и пунктуации
		sents_text_nf=[] # Список предложений с сохранением лишних пробелов без пунктуации
		# Пример: [[[0, 2], [4, 8], [10, 17]], [[34, 34], [36, 38], [40, 43]]]
		sents_pos=[] # Список позиций символов начала и конца слов, разбитый по предложениям
		sents_pos_sl=[] # Тот же список, но номера идут от начала строки
		sents_pos_nf=[] # Тот же список, но без учета пунктуации
		sents_pos_nf_sl=[] # Тот же список, но номера идут от начала строки без учета пунктуации
		#--------------------------------------------------------------------------
		# Truncate - удалить лишние пробелы, переносы строк. Однако, strip по строкам не делается.
		if Truncate:
			#text=tr_str(text)
			pass
		else:
			text=text.replace(wdlb,dlb)
		#--------------------------------------------------------------------------
		word=''
		k=0
		# В принципе, текст не должен быть пуст, но мы на всякий случай инициализируем i, чтобы не возникло ошибки при maxi=i
		i=0
		for i in range(len(text)):
			if text[i]==dlb:
				dlbs+=[i]
				# Проверка защищает от двойных dlb и пробелов
				if word!='':
					words.append(word)
				word=''
				nls+=[len(words)]
				k=-1
			# Необходимо разделять слова с неразрывным пробелом тоже, иначе фраза будет восприниматься как единое слово
			elif text[i].isspace():
				spaces+=[i]
				spaces_sl+=[k]
				if word!='':
					words.append(word)
				word=''
			else:
				word+=text[i]
				if len(word)==1:
					first_syms+=[i]
					first_syms_sl+=[k]
					if word.isdigit() or word.isalpha() or word in allowed_syms:
						first_syms_nf+=[i]
						first_syms_nf_sl+=[k]
					elif i+1 < len(text):
						delta=i+1
						kdelta=k+1
						while delta < len(text) and not text[delta].isalpha() and not text[delta].isdigit() and not text[delta] in allowed_syms:
							delta+=1
							kdelta+=1
						first_syms_nf+=[delta]
						first_syms_nf_sl+=[kdelta]
						log(cur_func,lev_debug,globs['mes'].first_syms_cor % (i,delta))
					else:
						first_syms_nf+=[i]
						first_syms_nf_sl+=[k]
						log(cur_func,lev_warn,globs['mes'].first_syms_failure)
			k+=1
		# Добавление последнего слова
		if word!='' and word!=dlb:
			words.append(word)
		maxi=i
		words_num=len(words)
		sent_no=0
		for i in range(words_num):
			words_nf.append(prepare_str(words[i],Extended=False)) # Ключ Extended=True удалит цифры
			last_syms+=[first_syms[i]+len(words[i])-1]
			last_syms_nf+=[first_syms_nf[i]+len(words_nf[i])-1]
			last_syms_sl+=[first_syms_sl[i]+len(words[i])-1]
			last_syms_nf_sl+=[first_syms_nf_sl[i]+len(words_nf[i])-1]
			if i in nls:
				sent_no+=1
			sent_nos+=[sent_no]
		#--------------------------------------------------------------------------	
		sent_no=0
		j=0
		pos_sl=[] # Список позиций всех символов в тексте в формате [[0,0],[0,1]...[n,n]]
		for i in range(maxi+1):
			pos_sl+=[[sent_no,j]]
			if i in dlbs:
				sent_no+=1
				j=0
			else:
				j+=1
		#--------------------------------------------------------------------------
		sents=[]
		sents_nf=[]
		old_sent_no=-1
		cur_sent=[]
		cur_sent_nf=[]
		cur_pos=[]
		cur_pos_nf=[]
		cur_pos_sl=[]
		cur_pos_nf_sl=[]
		for i in range(len(sent_nos)):
			sent_no=sent_nos[i]
			if sent_no!=old_sent_no:
				if cur_sent!=[]:
					sents+=[cur_sent]
				if cur_sent_nf!=[]:
					sents_nf+=[cur_sent_nf]
				if cur_pos!=[]:
					sents_pos+=[cur_pos]
				if cur_pos_nf!=[]:
					sents_pos_nf+=[cur_pos_nf]
				if cur_pos_sl!=[]:
					sents_pos_sl+=[cur_pos_sl]
				if cur_pos_nf_sl!=[]:
					sents_pos_nf_sl+=[cur_pos_nf_sl]
				cur_sent=[]
				cur_sent_nf=[]
				cur_pos=[]
				cur_pos_nf=[]
				cur_pos_sl=[]
				cur_pos_nf_sl=[]
				old_sent_no=sent_no
			cur_sent+=[words[i]]
			cur_sent_nf+=[words_nf[i]]
			cur_pos+=[[first_syms[i],last_syms[i]]]
			cur_pos_sl+=[[first_syms_sl[i],last_syms_sl[i]]]
			cur_pos_nf+=[[first_syms_nf[i],last_syms_nf[i]]]
			cur_pos_nf_sl+=[[first_syms_nf_sl[i],last_syms_nf_sl[i]]]
		#--------------------------------------------------------------------------
		# Добавление последнего предложения
		if cur_sent!=[]:
			sents+=[cur_sent]
		if cur_sent_nf!=[]:
			sents_nf+=[cur_sent_nf]
		if cur_pos!=[]:
			sents_pos+=[cur_pos]
		if cur_pos_nf!=[]:
			sents_pos_nf+=[cur_pos_nf]
		if cur_pos_sl!=[]:
			sents_pos_sl+=[cur_pos_sl]
		if cur_pos_nf_sl!=[]:
			sents_pos_nf_sl+=[cur_pos_nf_sl]
		#--------------------------------------------------------------------------
		# +1 к номеру последнего предложения
		sents_num=len(sents)
		#--------------------------------------------------------------------------
		for i in range(sents_num):
			if len(sents_pos_sl[i]) > 0:
				sents_sym_len+=[sents_pos_sl[i][-1][1]]
			else:
				sents_sym_len+=[0]
				log(cur_func,lev_warn,globs['mes'].zero_len_sent % i)
		#--------------------------------------------------------------------------
		# +1 к номеру последнего слова в предложении
		for i in range(sents_num):
			sents_word_len+=[len(sents_pos[i])]
		#--------------------------------------------------------------------------
		for i in range(sents_num):
			if sents_sym_len[i] > 0:
				dummy=' '*(sents_sym_len[i]-1)
			else:
				dummy=''
			dummy=list(dummy)
			dummy_nf=list(dummy)
			for j in range(sents_word_len[i]):
				pos1=sents_pos_sl[i][j][0]
				pos1_nf=sents_pos_nf_sl[i][j][0]
				pos2=sents_pos_sl[i][j][1]
				pos2_nf=sents_pos_nf_sl[i][j][1]
				dummy[pos1:pos2+1]=sents[i][j]
				dummy_nf[pos1_nf:pos2_nf+1]=sents_nf[i][j]
			sents_text+=[''.join(dummy)]
			sents_text_nf+=[''.join(dummy_nf)]
		#--------------------------------------------------------------------------
		detailed_declined=decline_nom(words_nf,Decline=Decline)
		#--------------------------------------------------------------------------
		assert(words_num==len(words))
		assert(words_num==len(words_nf))
		assert(words_num==len(first_syms))
		assert(words_num==len(first_syms_sl))
		assert(words_num==len(first_syms_nf))
		assert(words_num==len(first_syms_nf_sl))
		assert(words_num==len(last_syms))
		assert(words_num==len(last_syms_sl))
		assert(words_num==len(last_syms_nf))
		assert(words_num==len(last_syms_nf_sl))
		assert(sents_num==len(sents))
		assert(sents_num==len(sents_nf))
		assert(sents_num==len(sents_pos))
		assert(sents_num==len(sents_pos_nf))
		assert(sents_num==len(sents_pos_sl))
		assert(sents_num==len(sents_pos_nf_sl))
		assert(sents_num==len(sents_text))
		assert(sents_num==len(sents_text_nf))
		#--------------------------------------------------------------------------
		end_time=time()
		log(cur_func,lev_info,globs['mes'].analysis_finished % str(end_time-start_time))
		#--------------------------------------------------------------------------
		log(cur_func,lev_debug,'len (=maxi+1): %d' % (maxi+1))
		log(cur_func,lev_debug,'words: %s' % str(words))
		log(cur_func,lev_debug,'words_nf: %s' % str(words_nf))
		log(cur_func,lev_debug,'nls: %s' % str(nls))
		log(cur_func,lev_debug,'dlbs: %s' % str(dlbs))
		log(cur_func,lev_debug,'spaces: %s' % str(spaces))
		log(cur_func,lev_debug,'spaces_sl: %s' % str(spaces_sl))
		log(cur_func,lev_debug,'first_syms: %s' % str(first_syms))
		log(cur_func,lev_debug,'first_syms_sl: %s' % str(first_syms_sl))
		log(cur_func,lev_debug,'first_syms_nf: %s' % str(first_syms_nf))
		log(cur_func,lev_debug,'first_syms_nf_sl: %s' % str(first_syms_nf_sl))
		log(cur_func,lev_debug,'last_syms: %s' % str(last_syms))
		log(cur_func,lev_debug,'last_syms_sl: %s' % str(last_syms_sl))
		log(cur_func,lev_debug,'last_syms_nf: %s' % str(last_syms_nf))
		log(cur_func,lev_debug,'last_syms_nf_sl: %s' % str(last_syms_nf_sl))
		log(cur_func,lev_debug,'sent_nos: %s' % str(sent_nos))
		log(cur_func,lev_debug,'words_num: %d' % words_num)
		log(cur_func,lev_debug,'pos_sl: %s' % str(pos_sl))
		log(cur_func,lev_debug,'sents_num: %d' % sents_num)
		log(cur_func,lev_debug,'sents: %s' % str(sents))
		log(cur_func,lev_debug,'sents_nf: %s' % str(sents_nf))
		log(cur_func,lev_debug,'sents_pos: %s' % str(sents_pos))
		log(cur_func,lev_debug,'sents_pos_nf: %s' % str(sents_pos_nf))
		log(cur_func,lev_debug,'sents_pos_sl: %s' % str(sents_pos_sl))
		log(cur_func,lev_debug,'sents_pos_nf_sl: %s' % str(sents_pos_nf_sl))
		log(cur_func,lev_debug,'sents_sym_len: %s' % str(sents_sym_len))
		log(cur_func,lev_debug,'sents_word_len: %s' % str(sents_word_len))
		log(cur_func,lev_debug,'sents_text: %s' % str(sents_text))
		log(cur_func,lev_debug,'sents_text_nf: %s' % str(sents_text_nf))
		log(cur_func,lev_debug,'detailed_declined: %s' % str(detailed_declined))
		#--------------------------------------------------------------------------
		text_db={'len':maxi+1,'words_num':words_num,'words':words,'words_nf':words_nf,
				'first_syms':first_syms,'first_syms_nf':first_syms_nf,'first_syms_sl':first_syms_sl,
				'first_syms_nf_sl':first_syms_nf_sl,'last_syms':last_syms,'last_syms_sl':last_syms_sl,
				'last_syms_nf':last_syms_nf,'last_syms_nf_sl':last_syms_nf_sl,'nls':nls,'dlbs':dlbs,
				'spaces':spaces,'spaces_sl':spaces_sl,'sent_nos':sent_nos,'pos_sl':pos_sl,'text':text,
				'sents_num':sents_num,'sents_pos':sents_pos,'sents_pos_nf':sents_pos_nf,'sents':sents,
				'sents_nf':sents_nf,'sents_pos_sl':sents_pos_sl,'sents_pos_nf_sl':sents_pos_nf_sl,
				'sents_sym_len':sents_sym_len,'sents_word_len':sents_word_len,'sents_text':sents_text,
				'sents_text_nf':sents_text_nf,'declined':detailed_declined,'text':text}
		return text_db
		
# Преобразовать строку в нижний регистр, удалить пунктуацию и алфавитную нумерацию
def prepare_str(line,Extended=False):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		line=line.lower()
		line=line.replace('ё','е')
		line=line.replace('"','')
		line=line.replace('“','')
		line=line.replace('”','')
		line=line.replace('«','')
		line=line.replace('»','')
		line=line.replace('(','')
		line=line.replace(')','')
		line=line.replace('[','')
		line=line.replace(']','')
		line=line.replace('{','')
		line=line.replace('}','')
		line=line.replace('*','')
		line=delete_punctuation(line)
		line=delete_alphabetic_numeration(line)
		if Extended:
			line=re.sub('\d+','',line)
			#line=line.replace('-','')
		#log(cur_func,lev_debug,str(line))
	return line
	
# Удалить знаки пунктуации
# Это самый простой путь. Заменяет все совпадения (в отличие от использования переменных из punc_array) и не требует regexp (при котором потребуется экранирование)
def delete_punctuation(fragm):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		fragm=fragm.replace(',','')
		fragm=fragm.replace('.','')
		fragm=fragm.replace('!','')
		fragm=fragm.replace('?','')
		fragm=fragm.replace(':','')
		fragm=fragm.replace(';','')
		log(cur_func,lev_debug,str(fragm))
	return fragm
	
# Удалить нумерацию в виде алфавита
def delete_alphabetic_numeration(line):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		my_expr=' [\(,\[]{0,1}[aA-zZ,аА-яЯ][\.,\),\]]( \D)'
		match=re.search(my_expr,line)
		while match:
			replace_what=match.group(0)
			replace_with=match.group(1)
			line=line.replace(replace_what,replace_with)
			match=re.search(my_expr,line)
		log(cur_func,lev_debug,str(line))
	return line
	
# Создать кнопку с различными параметрами
# expand=1 - увеличить расстояние между кнопками
# Моментальная упаковка не поддерживается, потому что это действие возвращает вместо виджета None, а мы проводим далее над виджетом другие операции
def create_button(parent_widget,text,hint,action,expand=0,side='left',fg='black',Silent=False,Critical=True,width=None,height=None,bd=0,icon_path='',hint_delay=None,hint_width=None,hint_height=None,hint_background=None,hint_direction=None,hint_border_width=None,hint_border_color=None,bindings=[]):
	# side: must be 'top, 'bottom', 'left' or 'right'
	cur_func=sys._getframe().f_code.co_name
	button=None
	Success=True # Кнопку удалось инициализировать и упаковать; неудачные привязки не учитываются
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		bindings_type=get_obj_type(bindings,Verbal=True,IgnoreErrors=True)
		if bindings_type==globs['mes'].type_str or bindings_type==globs['mes'].type_lst:
			if bindings_type==globs['mes'].type_str:
				bindings=[bindings]
			if empty(width):
				width=globs['int']['default_button_size']
			if empty(height):
				height=globs['int']['default_button_size']
			if empty(hint_delay):
				hint_delay=globs['int']['default_hint_delay']
			if empty(hint_width):
				hint_width=globs['int']['default_hint_width']
			if empty(hint_height):
				hint_height=globs['int']['default_hint_height']
			if empty(hint_background):
				hint_background=globs['var']['default_hint_background']
			if empty(hint_direction):
				hint_direction=globs['var']['default_hint_direction']
			if empty(hint_border_width):
				hint_border_width=globs['int']['default_hint_border_width']
			if empty(hint_border_color):
				hint_border_color=globs['var']['default_hint_border_color']
			if not empty(bindings):
				# Наличие элемента #0 должно гарантироваться в empty
				hint_expand=dlb+bindings[0].replace('<','').replace('>','')
				i=1
				while i < len(bindings):
					hint_expand+=', '+bindings[i].replace('<','').replace('>','')
					i+=1
				hint+=hint_expand
			try:
				if empty(icon_path) or globs['bool']['TextButtons']:
					button=tk.Button(parent_widget,text=text,fg=fg)
				else:
					button_img=load_icon(icon_path=icon_path,parent_widget=parent_widget,width=width,height=height,Silent=Silent,Critical=Critical)
					button=tk.Button(parent_widget,image=button_img,width=width,height=height,bd=bd)
					button.flag_img=button_img
			except tk.TclError:
				Success=False
				if Critical:
					globs['AbortAll']=True
			try:
				button.pack(expand=expand,side=side)
			# tk.TclError, AttributeError
			except:
				Success=False
				if Critical:
					globs['AbortAll']=True
			create_binding(widget=button,bindings=['<Return>','<KP_Enter>','<space>','<ButtonRelease-1>'],action=action)
			log(cur_func,lev_debug,str(Success))
			if not Success:
				mestype(cur_func,globs['mes'].button_create_failed % text,Silent=Silent,Critical=Critical)
		else:
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(bindings_type),'%s, %s' % (globs['mes'].type_str,globs['mes'].type_lst)))
	return button
	
# Выделить весь текст в виджете
def select_all(widget,Small=True): # Entry: Small=True; Text: Small=False
	if Small:
		widget.select_clear()
		widget.select_range(0,'end')
	else:
		widget.tag_add('sel','1.0','end')
		widget.mark_set('insert','1.0')
	return 'break'
	
# Вернуть расширение файла с точкой
def get_ext(file,Lower=False):
	cur_func=sys._getframe().f_code.co_name
	func_res=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		func_res=os.path.splitext(file)[1]
		if Lower:
			func_res=func_res.lower()
		log(cur_func,lev_debug,str(func_res))
	return func_res
	
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# non-shared code
# Get a non-word nearest to the selected word and a corresponding non-word in the second pane
def get_right_border(text11_db,text22_db,txt):
	cur_func = sys._getframe().f_code.co_name
	stone_no1 = 0
	stone_no2 = 0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		cursor_pos = get_cursor(widget=txt)
		cursor_pos = tk2pos(text11_db,cursor_pos,Even=False)
		get_word_by_pos(text11_db,cursor_pos)
		stone_no1 = get_relation(text11_db)
		stone1 = text11_db['words_nf'][stone_no1]
		get_repetitions(text11_db,stone_no1)
		stone_rep1 = 0
		if len(text11_db['nw_repetitions'][stone_no1]) > 1:
			log(cur_func,lev_debug,globs['mes'].repetitions % (text11_db['words'][stone_no1],stone_no1,str(text11_db['nw_repetitions'][stone_no1])))
			stone_rep1 = get_closest(text11_db['nw_repetitions'][stone_no1],text11_db['word_no'])
			log(cur_func,lev_debug,globs['mes'].cursor_word % (text11_db['words'][stone_no1],stone_no1,stone_rep1))
		else:
			log(cur_func,lev_debug,globs['mes'].no_repetitions % (text11_db['words'][stone_no1],stone_no1))
		# Note: words_nf treats '(2)' as '2' 
		try:
			stone_no2 = text22_db['words_nf'].index(stone1)
		except ValueError:
			if 'word_no' in text22_db:
				stone_no2 = text22_db['word_no']
			else:
				stone_no2 = 0
		get_repetitions(text22_db,stone_no2)
		# +1 due to len()
		if len(text22_db['nw_repetitions'][stone_no2]) >= stone_rep1 + 1:
			log(cur_func,lev_debug,globs['mes'].repetitions % (text22_db['words'][stone_no2],stone_no2,str(text22_db['nw_repetitions'][stone_no2])))
			stone_rep2 = stone_rep1
			stone_no2 = text22_db['nw_repetitions'][stone_no2][stone_rep2]
		elif len(text22_db['nw_repetitions'][stone_no2]) > 0:
			stone_rep2 = 0
			stone_no2 = text22_db['nw_repetitions'][stone_no2][stone_rep2]
			log(cur_func,lev_debug,globs['mes'].no_repetitions % (text22_db['words'][stone_no2],stone_no2))
		else:
			stone_rep2 = 0
		log(cur_func,lev_info,globs['mes'].related_words % (text11_db['words'][stone_no1],stone_no1,stone_rep1,text22_db['words'][stone_no2],stone_no2,stone_rep2))
	return(stone_no1,stone_no2)

# Get a cursor position in the original and set a corresponding position in the translation
# It may be a not very good idea to have calculations directly in a graphics function, however, building lists with all possible matches is VERY time-consuming on long texts
def compare_gui(text1_db,text2_db):
	def compare_callback1():
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			stones = get_right_border(text1_db,text2_db,txt1)
			stone_no1 = stones[0]
			stone_no2 = stones[1]
			if stone_no1 != -1:
				fragm_start = text1_db['first_syms'][stone_no1]
				fragm_end = text1_db['last_syms'][stone_no1]
				# Remove all tags
				tag_remove(txt1,'txt1tag','1.0','end')
				tag_remove(txt2,'txt2tag','1.0','end')
				# Set tags for the first pane
				fragm_start = pos2tk(text1_db,fragm_start,Even=False)
				fragm_end = pos2tk(text1_db,fragm_end,Even=True)
				tag_add_config(txt1,'txt1tag',fragm_start,fragm_end,mode='bg',color='cyan')
			if stone_no2 != -1:
				# Set tags for the second pane
				fragm_start = text2_db['first_syms'][stone_no2]
				fragm_end = text2_db['last_syms'][stone_no2]
				lift_pos = fragm_start
				if globs['bool']['UseHeadInterval']:
					# Experimentally supported values
					if lift_pos - 1000 >= 0:
						lift_pos -= 1000
				fragm_start = pos2tk(text2_db,fragm_start,Even=False)
				lift_pos = pos2tk(text2_db,lift_pos,Even=False)
				fragm_end = pos2tk(text2_db,fragm_end,Even=True)
				tag_add_config(txt2,'txt2tag',fragm_start,fragm_end,mode='bg',color='orange')
				mark_add(txt2,'insert',fragm_start)
				# Remember the last successful/found selection
				cursor_pos = get_cursor(txt2,pane_no=2)
				cursor_pos = tk2pos(text2_db,cursor_pos,Even=False)
				get_word_by_pos(text2_db,cursor_pos)
				drag_screen(txt2,lift_pos,pane_no=2)
	def compare_callback2():
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			stones = get_right_border(text2_db,text1_db,txt2)
			stone_no2 = stones[0]
			stone_no1 = stones[1]
			if stone_no1 != -1:
				fragm_start = text2_db['first_syms'][stone_no2]
				fragm_end = text2_db['last_syms'][stone_no2]
				# Remove all tags
				tag_remove(txt1,'txt1tag','1.0','end')
				tag_remove(txt2,'txt2tag','1.0','end')
				# Set tags for the first pane
				fragm_start = pos2tk(text2_db,fragm_start,Even=False)
				fragm_end = pos2tk(text2_db,fragm_end,Even=True)
				tag_add_config(txt2,'txt2tag',fragm_start,fragm_end,mode='bg',color='cyan')
			if stone_no2 != -1:
				# Set tags for the second pane
				fragm_start = text1_db['first_syms'][stone_no1]
				fragm_end = text1_db['last_syms'][stone_no1]
				lift_pos = fragm_start
				if globs['bool']['UseHeadInterval']:
					# Experimentally supported values
					if lift_pos - 1000 >= 0:
						lift_pos -= 1000
				fragm_start = pos2tk(text1_db,fragm_start,Even=False)
				lift_pos = pos2tk(text1_db,lift_pos,Even=False)
				fragm_end = pos2tk(text1_db,fragm_end,Even=True)
				tag_add_config(txt1,'txt1tag',fragm_start,fragm_end,mode='bg',color='orange')
				mark_add(txt1,'insert',fragm_start)
				# Remember the last successful/found selection
				cursor_pos = get_cursor(txt1,pane_no=1)
				cursor_pos = tk2pos(text1_db,cursor_pos,Even=False)
				get_word_by_pos(text1_db,cursor_pos)
				drag_screen(txt1,lift_pos,pane_no=1)
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		top = tk.Toplevel(root)
		top.title(globs['mes'].comparison)
		if globs['bool']['AlwaysMaximize']:
			if sys_type=='lin':
				top.wm_attributes('-zoomed',True)
			# Win, Mac
			else:
				top.wm_state(newstate='zoomed')
		frame1 = tk.Frame(top)
		frame2 = tk.Frame(top)
		frame1.pack(expand=1,fill='both',side='left')
		frame2.pack(expand=1,fill='both',side='right')
		scrollbar1 = tk.Scrollbar(frame1)
		scrollbar2 = tk.Scrollbar(frame2)
		scrollbar1.pack(side='right',fill='y')
		scrollbar2.pack(side='right',fill='y')
		# Setting a font manually may result in showing ownly the first frame or non-equal first and second pane dimensions - a tkinter bug?
		#,font='Serif 14'
		txt1 = tk.Text(frame1,wrap='word',font='Arial 12',yscrollcommand=scrollbar1.set)
		txt1.pack(expand=1,fill='both')
		txt2 = tk.Text(frame2,wrap='word',font='Arial 12',yscrollcommand=scrollbar2.set)
		txt2.pack(expand=1,fill='both')
		scrollbar1.config(command=txt1.yview)
		scrollbar2.config(command=txt2.yview)
		txt1.insert('end',text1_db['text'])
		txt2.insert('end',text2_db['text'])
		txt1.focus_force()
		if text1_db['words_num'] > 0:
			word_pos = text1_db['first_syms'][0]
			word_pos = pos2tk(text1_db,word_pos,Even=False)
			mark_add(txt1,'insert',word_pos)
		else:
			mark_add(txt1,'insert','1.0')
		create_binding(widget=txt1,bindings=['<Return>','<KP_Enter>','<ButtonRelease-1>','<Left>','<Right>','<Up>','<Down>','<Prior>','<Next>','<Control-Left>','<Control-Right>','<Home>','<End>','<Control-Home>','<Control-End>'],action=lambda e: compare_callback1())
		create_binding(widget=txt2,bindings=['<Return>','<KP_Enter>','<ButtonRelease-1>','<Left>','<Right>','<Up>','<Down>','<Prior>','<Next>','<Control-Left>','<Control-Right>','<Home>','<End>','<Control-Home>','<Control-End>'],action=lambda e: compare_callback2())
		# Search the first pane
		#create_button(parent_widget=txt1,text=globs['mes'].btn_search,hint=globs['mes'].hint_search_article,action=lambda e:search_pane(text1_db,txt1,direction='clear'),icon_path=globs['var']['icon_search_article'],bindings=globs['var']['bind_re_search_article'])
		create_binding(widget=txt1,bindings=globs['var']['bind_search_article_forward'],action=lambda e:search_pane(text1_db,txt1,direction='forward',pane_no=1))
		create_binding(widget=txt1,bindings=globs['var']['bind_search_article_backward'],action=lambda e:search_pane(text1_db,txt1,direction='backward',pane_no=1))
		create_binding(widget=txt1,bindings=globs['var']['bind_re_search_article'],action=lambda e:search_pane(text1_db,txt1,direction='clear',pane_no=1))
		# Search the second pane
		create_binding(widget=txt2,bindings=globs['var']['bind_search_article_forward'],action=lambda e:search_pane(text2_db,txt2,direction='forward',pane_no=2))
		create_binding(widget=txt2,bindings=globs['var']['bind_search_article_backward'],action=lambda e:search_pane(text2_db,txt2,direction='backward',pane_no=2))
		create_binding(widget=txt2,bindings=globs['var']['bind_re_search_article'],action=lambda e:search_pane(text2_db,txt2,direction='clear',pane_no=2))
		compare_callback1()
		top.wait_window()
	
# Append numbers of words that do not contain any Russian or Latin letters ('non-words') to the database
def add_non_words(text_db):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		text_db['nw_nos'] = []
		text_lang = langdet_profound(text_db['text'],Strict=False,Verbose=False)
		for i in range(text_db['words_num']):
			IsWord = True
			# Otherwise, all empty entries will be considered as non-words instead of, e.g., digits.
			# Check for spaces if Truncate == False
			if empty(text_db['words_nf'][i]) or text_db['words_nf'][i] == ' ':
				pass
			else:
				# You can't find words that are of a 'mixed' type (comprising Cyrillic and Latin letters) in the translation, so it is better to check whether the word is 'lat'
				word_lang = langdet(text_db['words_nf'][i])
				if text_lang == 'ru' and word_lang == 'lat' or word_lang == 'none':
					IsWord = False
			if not IsWord:
				text_db['nw_nos'].append(i)
		text_db['nw_nos_num'] = len(text_db['nw_nos'])
	return text_db
	
# Get a nearest non-word to the right
def get_relation(text_db):
	cur_func = sys._getframe().f_code.co_name
	j = 0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		assert text_db['word_no'] < text_db['words_num']
		j = text_db['word_no']
		while not j in text_db['nw_nos'] and j < text_db['words_num']-1:
			j += 1
	return j

# Create a list of occurrences of an element in a list
def get_repetitions(text_db,word_no):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		text_db['nw_repetitions'] = []
		for i in range(text_db['words_num']):
			text_db['nw_repetitions'] += [[]]
		add_item = []
		for i in range(text_db['words_num']):
			if text_db['words_nf'][i] == text_db['words_nf'][word_no]:
				add_item.append(i)
		for i in range(len(add_item)):
			text_db['nw_repetitions'][add_item[i]] = add_item
		assert len(text_db['nw_repetitions']) == text_db['words_num']
	
# Make a manual comparison of parallel texts more intuitive
def compare_parallel_texts(orig_file,transl_file,MakePretty=True,Silent=False,Critical=True):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if exist(orig_file,Silent=Silent,Critical=Critical) and exist(transl_file,Silent=Silent,Critical=Critical):
			# Files may be ovewritten to have UTF-8 encoding!
			text1 = load_file(orig_file)
			text2 = load_file(transl_file)
			#------------------------------------------------------------------
			if MakePretty:
				# Rearrange texts to make them look prettier in the plain text widget
				text1 = text1.splitlines()
				for i in range(len(text1)):
					text1[i] = text1[i].strip()
					text1[i] = tab + text1[i]
				text1 = dlb.join(text1)
			#------------------------------------------------------------------
				text2 = text2.splitlines()
				for i in range(len(text2)):
					text2[i] = text2[i].strip()
					text2[i] = tab + text2[i]
				text2 = dlb.join(text2)
			#------------------------------------------------------------------
			text1_db = analyse_text(text1,Truncate=False)
			text2_db = analyse_text(text2,Truncate=False)
			#------------------------------------------------------------------
			if text1_db['sents_num'] != text2_db['sents_num']:
				log(cur_func,lev_warn,globs['mes'].unequal_number_of_sentences % (text1_db['sents_num'],text2_db['sents_num']))
			#------------------------------------------------------------------
			text1_db = add_non_words(text1_db)
			text2_db = add_non_words(text2_db)
			#------------------------------------------------------------------
			root.withdraw()
			compare_gui(text1_db,text2_db)
			#root.deiconify()
			sys.exit()

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Standalone code (2)

sys_type = detect_os()

if sys_type == 'lin':
	sysdiv = '/'
elif sys_type == 'win':
	sysdiv = '\\'
elif sys_type == 'mac':
	sysdiv = '/'
dlb_os = 'UNIX'

globs = {}
globs['AbortAll'] = False
globs['bool'] = {'UseHeadInterval':True,'AlwaysMaximize':False,'Spelling':False,'UnixSelection':False,'TextButtons':True,'DeleteBOM':True}
globs['bin_dir'] = true_dirname(os.path.realpath(sys.argv[0]),UseLog=False)
globs['mes'] = mes_ru
globs['var'] = {'bind_search_article_forward':'<F3>','bind_search_article_backward':'<Shift-F3>','bind_re_search_article':'<Control-F3>','font_style':'Arial 12','default_hint_background':'#ffffe0','default_hint_direction':'top','default_hint_border_color':'navy'}
globs['int'] = {'default_button_size':36,'default_hint_delay':800,'default_hint_width':280,'default_hint_height':40,'default_hint_border_width':1}
my_program_title = ''

root = tk.Tk()
root.title(globs['mes'].wait)

mode = 'args' # 'args', 'manual'

if len(sys.argv) > 2:
	mode = 'args'
	orig_file = sys.argv[1]
	transl_file = sys.argv[2]
else:
	mode = 'manual'
	curdir = os.path.expanduser('~')
	if not os.path.exists(curdir):
		curdir = globs['bin_dir']
		exist(curdir)
	orig_file = dialog_open_file(dir=curdir,my_title=globs['mes'].select_file1,mask='.txt')

if not empty(orig_file):
	if not get_ext(orig_file,Lower=True) == '.txt':
		ErrorMessage(cur_mes=globs['mes'].only_txt)
	if mode == 'manual':
		curdir = true_dirname(orig_file)
		transl_file = dialog_open_file(dir=curdir,my_title=globs['mes'].select_file2,mask='.txt')
	if not empty(transl_file):
		if not get_ext(transl_file,Lower=True) == '.txt':
			ErrorMessage(cur_mes=globs['mes'].only_txt)
		compare_parallel_texts(orig_file,transl_file)
root.mainloop()
