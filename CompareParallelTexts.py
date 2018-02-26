#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','./locale')

import shared    as sh
import sharedGUI as sg


# Requires 'refs'
def synchronize(event=None):
    tkpos    = panes.pane1.cursor()
    word_no  = refs.words1.no_by_tk(tkpos=tkpos)
    sword_no = refs.nearest_ref(word_no=word_no)
    
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




if __name__ == '__main__':
    sg.objs.start()
    panes = sg.Panes()
    
    file1 = '/tmp/orig all - ru.txt'
    file2 = '/tmp/orig all - en (OCR).txt'

    text1 = sh.ReadTextFile(file1).get()
    text2 = sh.ReadTextFile(file2).get()

    text1 = sh.Text(text=text1,Auto=True).text
    text2 = sh.Text(text=text2,Auto=True).text
    
    words1 = sh.Words (text = text1
                      ,Auto = False
                      )
    words2 = sh.Words (text = text2
                      ,Auto = False
                      )
    
    refs = sh.References (words1 = words1
                         ,words2 = words2
                         )
    
    panes.reset (words1 = refs.words1
                ,words2 = refs.words2
                )
                
    panes.pane1.insert(text1)
    panes.pane2.insert(text2)
    
    sg.bind (obj      = panes.pane1
            ,bindings = '<ButtonRelease-1>'
            ,action   = synchronize
            )
    
    panes.show()
    sg.objs.end()