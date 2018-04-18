#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import easygui   as eg
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('CompareParallelTexts','../resources/locale')


# Requires 'refs'
def synchronize(event=None):
    tkpos    = panes.pane1.cursor()
    word_no  = refs.words1.no_by_tk(tkpos=tkpos)
    word_no  = sh.Input (title = 'synchronize'
                        ,value = word_no
                        ).integer()
    sword_no = refs.nearest_ref(word_no=word_no)
    sword_no = sh.Input (title = 'synchronize'
                        ,value = sword_no
                        ).integer()
    
    sword_no2 = refs.repeated2 (word_n = refs.words1.words[sword_no]._n
                               ,count  = refs.repeated(word_no=sword_no)
                               )
    
    cur_mark = refs.words1.words[word_no].tf()
    ref_mark = refs.words1.words[sword_no].tf()
    
    panes.pane1.tag_add (tag_name = 'current'
                        ,pos1tk   = cur_mark
                        ,pos2tk   = refs.words1.words[word_no].tl()
                        )
    panes.pane1.tag_add (tag_name = 'ref'
                        ,pos1tk   = ref_mark
                        ,pos2tk   = refs.words1.words[sword_no].tl()
                        )
    panes.pane1.tag_config (tag_name   = 'current'
                           ,background = 'green'
                           )
    panes.pane1.tag_config (tag_name   = 'ref'
                           ,background = 'cyan'
                           )
    
    panes.pane1.see(ref_mark)
    panes.pane1.see(cur_mark)
    
    if sword_no2 is None:
        sh.log.append ('synchronize'
                      ,_('WARNING')
                      ,_('Cannot set a reference!')
                      )
    else:
        ref_mark2 = refs.words2.words[sword_no2].tf()
        panes.pane2.tag_add (tag_name = 'ref'
                            ,pos1tk   = ref_mark2
                            ,pos2tk   = refs.words2.words[sword_no2].tl()
                            )
        panes.pane2.tag_config (tag_name   = 'ref'
                               ,background = 'cyan'
                               )
        panes.pane2.see(ref_mark2)
    panes.select1()




if __name__ == '__main__':
    sg.objs.start()

    file1 = eg.fileopenbox (title     = _('Load 1st text (Cyrillic characters)')
                           ,filetypes = ['*.txt']
                           )
                           
    if sh.File(file=file1).Success:
        file2 = eg.fileopenbox (title     = _('Load 2nd text (Latin characters)')
                               ,default   = file1
                               ,filetypes = ['*.txt']
                               )
        if sh.File(file=file2).Success:
            text1 = sh.ReadTextFile(file1).get()
            text2 = sh.ReadTextFile(file2).get()

            text1 = sh.Text(text=text1,Auto=True).text
            text2 = sh.Text(text=text2,Auto=True).text
            
            text1 = text1.splitlines()
            text2 = text2.splitlines()
            
            text1 = ['\t' + line for line in text1]
            text2 = ['\t' + line for line in text2]
            
            text1 = '\n'.join(text1)
            text2 = '\n'.join(text2)
            
            if text1 and text2:
                words1 = sh.Words (text = text1
                                  ,Auto = False
                                  )
                words2 = sh.Words (text = text2
                                  ,Auto = False
                                  )
                refs = sh.References (words1 = words1
                                     ,words2 = words2
                                     )
                
                panes = sg.Panes()
                panes.reset (words1 = refs.words1
                            ,words2 = refs.words2
                            )
                            
                panes.pane1.insert(text1)
                panes.pane2.insert(text2)
                
                sg.bind (obj      = panes.pane1
                        ,bindings = '<ButtonRelease-1>'
                        ,action   = synchronize
                        )
                sg.bind (obj      = panes.pane2
                        ,bindings = '<ButtonRelease-1>'
                        ,action   = panes.select2
                        )
                
                panes.show()
            else:
                sg.Message ('CompareParallelTexts'
                           ,_('WARNING')
                           ,_('Empty input is not allowed!')
                           )
    # Do not use 'sg.objs.end()' - this interferes with 'easygui'
    sg.objs.root().kill()
