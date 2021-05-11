from jinja2 import Environment, BaseLoader

# template_t = """
#     <OnePrim SourceT11ID="112534" X="{{x + 40}}" Y="{{y}}" WIDTH="280" HEIGHT="20" OBJTYPE="1" GRNUM="0" DRAWTYPE="32834" PenParams="1" PenColor="12632256" BrushColor="12632256" GradColor="12632256" ScriptName="">
#       <PARAMS>[TEXT]={{text}}
# [FONTID]=19
# [USERFONT]=10;Arial;1;0;
# [HINT]=
# [DELTAST]=0</PARAMS>
#       <FONTID_EXDATA>РњРµРЅСЋ (С‡РµСЂРЅС‹Р№)/Arial/10/0/1</FONTID_EXDATA>
#     </OnePrim>
#     <OnePrim SourceT11ID="112535" X="{{x + 10}}" Y="{{y}}" WIDTH="20" HEIGHT="20" OBJTYPE="2" GRNUM="112535" DRAWTYPE="0" PenParams="1" PenColor="0" BrushColor="12632256" GradColor="536870911" ScriptName="">
#       <PARAMS>[HINT]=</PARAMS>
#     </OnePrim>
#     <OnePrim SourceT11ID="112536" X="{{x + 10}}" Y="{{y}}" WIDTH="20" HEIGHT="20" OBJTYPE="2" GRNUM="112535" DRAWTYPE="256" PenParams="1" PenColor="0" BrushColor="65280" GradColor="536870911" ScriptName="">
#       <PARAMS>[HINT]=</PARAMS>
#       <Animators>
#         <OneAnim ATRIBID="1" PARAMID="15626" OPER="1" CONSTVALUE="1" ACTPARAM="1" VARERROR="0" SCRIPTMODE="0" SCRIPTTEXT="" ARRAYPARAMS="0" PARAMMODE="0">
#           <ExData>({{text}})</ExData>
#           <ExDataA/>
#         </OneAnim>
#       </Animators>
#     </OnePrim>
# """

# template_t = """<OnePrim SourceT11ID="120500" PanelLayerNum="1" X="236" Y="{{y + 160}}" WIDTH="80" HEIGHT="20" OBJTYPE="1" GRNUM="0" DRAWTYPE="4" PenParams="1" PenColor="0" BrushColor="12632256" GradColor="0" ScriptName="OBJ_U1">
#       <PARAMS>[TEXT]=0,00
# [FONTID]=19
# [USERFONT]=10;Arial;1;0;
# [HINT]=
# [DELTAST]=2</PARAMS>
#       <Animators>
#         <OneAnim ATRIBID="8" PARAMID="15789" OPER="0" CONSTVALUE="0" ACTPARAM="" VARERROR="$NOCHANGE" SCRIPTMODE="0" SCRIPTTEXT="" ARRAYPARAMS="0" PARAMMODE="0">
#           <ExData>({{text}})</ExData>
#           <ExDataA/>
#         </OneAnim>
#         <OneAnim ATRIBID="2" PARAMID="15789" OPER="1" CONSTVALUE="1" ACTPARAM="16711935" VARERROR="14146783" SCRIPTMODE="0" SCRIPTTEXT="" ARRAYPARAMS="0" PARAMMODE="1">
#           <ExData>({{text}})</ExData>
#           <ExDataA/>
#         </OneAnim>
#       </Animators>
#       <FONTID_EXDATA>РњРµРЅСЋ (С‡РµСЂРЅС‹Р№)/Arial/10/0/1</FONTID_EXDATA>
#     </OnePrim>"""

# AI
# template_t = """<OnePrim SourceT11ID="112013" PanelLayerNum="1" X="346" Y="{{y + 40}}" WIDTH="229" HEIGHT="20" OBJTYPE="1" GRNUM="0" DRAWTYPE="2" PenParams="1" PenColor="12632256" BrushColor="12632256" GradColor="12632256" ScriptName="">
#       <PARAMS>[TEXT]={{text}}
# [FONTID]=19
# [USERFONT]=10;Arial;1;0;
# [HINT]=
# [DELTAST]=0</PARAMS>
#       <FONTID_EXDATA>РњРµРЅСЋ (С‡РµСЂРЅС‹Р№)/Arial/10/0/1</FONTID_EXDATA>
#     </OnePrim>
#     <OnePrim SourceT11ID="121334" PanelLayerNum="1" X="576" Y="{{y + 40}}" WIDTH="80" HEIGHT="20" OBJTYPE="1" GRNUM="0" DRAWTYPE="4" PenParams="1" PenColor="0" BrushColor="12632256" GradColor="0" ScriptName="">
#       <PARAMS>[TEXT]=0,00
# [FONTID]=19
# [USERFONT]=10;Arial;1;0;
# [HINT]=
# [DELTAST]=2</PARAMS>
#       <Animators>
#         <OneAnim ATRIBID="8" PARAMID="15778" OPER="0" CONSTVALUE="0" ACTPARAM="" VARERROR="$NOCHANGE" SCRIPTMODE="0" SCRIPTTEXT="" ARRAYPARAMS="0" PARAMMODE="0">
#           <ExData>({{text}})</ExData>
#           <ExDataA/>
#         </OneAnim>
#         <OneAnim ATRIBID="2" PARAMID="15778" OPER="1" CONSTVALUE="1" ACTPARAM="16711935" VARERROR="14146783" SCRIPTMODE="0" SCRIPTTEXT="" ARRAYPARAMS="0" PARAMMODE="1">
#           <ExData>({{text}})</ExData>
#           <ExDataA/>
#         </OneAnim>
#       </Animators>
#       <FONTID_EXDATA>РњРµРЅСЋ (С‡РµСЂРЅС‹Р№)/Arial/10/0/1</FONTID_EXDATA>
#     </OnePrim>
# """
# DI
template_t =  """
    <OnePrim SourceT11ID="121532" X="{{x + 30}}" Y="{{y + 10}}" WIDTH="285" HEIGHT="20" OBJTYPE="1" GRNUM="0" DRAWTYPE="2" PenParams="1" PenColor="12632256" BrushColor="12632256" GradColor="12632256" ScriptName="">
      <PARAMS>[TEXT]={{text}}
[FONTID]=19
[USERFONT]=10;Arial;1;0;
[HINT]=
[DELTAST]=0</PARAMS>
      <FONTID_EXDATA>РњРµРЅСЋ (С‡РµСЂРЅС‹Р№)/Arial/10/0/1</FONTID_EXDATA>
    </OnePrim>
    <OnePrim SourceT11ID="121533" X="{{x}}" Y="{{y + 10}}" WIDTH="20" HEIGHT="20" OBJTYPE="2" GRNUM="0" DRAWTYPE="0" PenParams="1" PenColor="0" BrushColor="12632256" GradColor="536870911" ScriptName="">
      <PARAMS>[HINT]=</PARAMS>
    </OnePrim>
    <OnePrim SourceT11ID="121549" X="{{x}}" Y="{{y + 10}}" WIDTH="20" HEIGHT="20" OBJTYPE="2" GRNUM="0" DRAWTYPE="256" PenParams="1" PenColor="0" BrushColor="65535" GradColor="536870911" ScriptName="OBJ_ERR_00">
      <PARAMS>[HINT]=</PARAMS>
      <Animators>
        <OneAnim ATRIBID="1" PARAMID="15583" OPER="1" CONSTVALUE="1" ACTPARAM="1" VARERROR="2" SCRIPTMODE="0" SCRIPTTEXT="" ARRAYPARAMS="0" PARAMMODE="0">
          <ExData>({{text}})</ExData>
          <ExDataA/>
        </OneAnim>
      </Animators>
    </OnePrim>
    <OnePrim SourceT11ID="121553" X="{{x}}" Y="{{y + 10}}" WIDTH="20" HEIGHT="20" OBJTYPE="2" GRNUM="0" DRAWTYPE="256" PenParams="1" PenColor="0" BrushColor="16711935" GradColor="536870911" ScriptName="">
      <PARAMS>[HINT]=</PARAMS>
      <Animators>
        <OneAnim ATRIBID="1" PARAMID="15583" OPER="1" CONSTVALUE="1" ACTPARAM="1" VARERROR="2" SCRIPTMODE="0" SCRIPTTEXT="" ARRAYPARAMS="0" PARAMMODE="0">
          <ExData>({{text}})</ExData>
          <ExDataA/>
        </OneAnim>
      </Animators>
    </OnePrim>
"""

data = """20	45	[РЇ1] РўРµР».РЎР’ РІС‹РєР°С‡.
20	70	[РЇ9] РЎР’ РѕС‚РєР»СЋС‡РµРЅ
20	95	[РЇ10] РЎР’ РІРєР»СЋС‡РµРЅ
20	120	[РЇ12] Р’РєР».РѕС‚ РђР’Р  РЎР’
20	145	[РЇ13] РћС‚РєР».РѕС‚ Р’РќР  РЎР’
20	170	[РЇ14] Р’РєР».РѕС‚ РђР’Р  РђР’
20	195	[РЇ15] РћС‚РєР».РѕС‚ Р·Р°С‰.Р’Р’
20	220	[РЇ16] РћС‚РєР».РѕС‚ Р·Р°С‰.РђР’
20	245	[РЇ17] Р”РЈ
20	270	[РЇ18] РђР’Р  РЎР’ РІРєР»-С‚СЊ
20	295	[РЇ19] РђР’Р  РЎР’ РѕС‚РєР»-С‚СЊ
20	320	[Рљ18] РђРІР°СЂ. РѕС‚РєР».
20	345	РђР’Р  РЎР’ РІРєР»СЋС‡РµРЅ
20	370	Р РµР»Рµ Р’С‹Р·oРІ
20	395	Р’С‹Р·РѕРІ Р’РєР». РїРѕ РђР’Р 
20	420	РћС‚РєР°Р· Р‘РњРџРђ""".split('\n')

template1 = Environment(loader=BaseLoader).from_string(template_t)

contents = []
for dat in data:
    x, y, text = dat.split('\t')
    x=int(x)
    y=int(y)
    contents.append(str(
        template1.render(text=text, x=x, y=y)))

print('\n'.join(contents))
