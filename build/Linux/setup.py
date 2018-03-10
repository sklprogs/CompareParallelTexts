from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict (packages = []
                    ,includes = ["re","easygui"]
                    ,excludes = []
                    )

executables = [Executable ('CompareParallelTexts.py'
                          ,base = 'Console'
                          ,icon = 'resources/icon_64x64_cpt.gif'
                          ,targetName = 'CompareParallelTexts'
                          )
              ]

setup (name        = 'CompareParallelTexts'
      ,version     = '1'
      ,description = 'Easily browse and compare parallel (original and translated) texts'
      ,options     = dict(build_exe=buildOptions)
      ,executables = executables
      )
