import numpy as np
from flask import Flask, redirect, url_for, render_template, request, Response, abort
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_utils import *
import json
import pickle
import pandas as pd
import multiprocessing as mp


app = Flask(__name__)
app.url_map.converters['list'] = ListConverter

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/kresult/<list:argus>')
@login_required
def keysearch(argus):
    import time
    print(argus)
    keyword, max_res = argus
    max_res = int(max_res)
    start_time = time.time()

    pool = mp.Pool(processes=(mp.cpu_count() - 1))
    # results = pool.map(worker, [(keyword, 9), (keyword, 901), (keyword, 902)]) #, (keyword, 903), (keyword, 904),
    #                            (keyword, 905), (keyword, 906), (keyword, 907), (keyword, 908), (keyword, 909)])
    # results = pool.map(worker, [(keyword, 9)])
    big_search = False
    if keyword == 'oncology':
        joined_result = pd.read_pickle('./publications_oncology.pkl')
        joined_result = joined_result.sort_values(by='pudmid', ascending=False)
    elif keyword == 'melanoma':
        joined_result = pd.read_pickle('./publications_melanoma.pkl')
        joined_result = joined_result.sort_values(by='pudmid', ascending=False)
    elif keyword == 'diabetic retinopathy':
        joined_result = pd.read_pickle('./publications_diabetic_retinopathy.pkl')
        joined_result = joined_result.sort_values(by='pudmid', ascending=False)

    elif big_search:
        '''
        print('Results 0')
        result0 = pool.map(search_dataframe,
                           [(keyword, '001'), (keyword, '002'), (keyword, '003'), (keyword, '004'),
                            (keyword, '005'), (keyword, '006'), (keyword, '007'), (keyword, '008'), (keyword, '009'),
                            (keyword, '010'), (keyword, '011'), (keyword, '012'), (keyword, '013'), (keyword, '014'),
                            (keyword, '015'), (keyword, '016'), (keyword, '017'), (keyword, '018'), (keyword, '019'),
                            (keyword, '020'), (keyword, '021'), (keyword, '022'), (keyword, '023'), (keyword, '024'),
                            (keyword, '025'), (keyword, '026'), (keyword, '027'), (keyword, '028'), (keyword, '029'),
                            (keyword, '030'), (keyword, '031'), (keyword, '032'), (keyword, '033'), (keyword, '034'),
                            (keyword, '035'), (keyword, '036'), (keyword, '037'), (keyword, '038'), (keyword, '039'),
                            (keyword, '040'), (keyword, '041'), (keyword, '042'), (keyword, '043'), (keyword, '044'),
                            (keyword, '045'), (keyword, '046'), (keyword, '047'), (keyword, '048'), (keyword, '049'),
                            (keyword, '050'), (keyword, '051'), (keyword, '052'), (keyword, '053'), (keyword, '054'),
                            (keyword, '055'), (keyword, '056'), (keyword, '057'), (keyword, '058'), (keyword, '059'),
                            (keyword, '060'), (keyword, '061'), (keyword, '062'), (keyword, '063'), (keyword, '064'),
                            (keyword, '065'), (keyword, '066'), (keyword, '067'), (keyword, '068'), (keyword, '069'),
                            (keyword, '070'), (keyword, '071'), (keyword, '072'), (keyword, '073'), (keyword, '074'),
                            (keyword, '075'), (keyword, '076'), (keyword, '077'), (keyword, '078'), (keyword, '079'),
                            (keyword, '080'), (keyword, '081'), (keyword, '082'), (keyword, '083'), (keyword, '084'),
                            (keyword, '085'), (keyword, '086'), (keyword, '087'), (keyword, '088'), (keyword, '089'),
                            (keyword, '090'), (keyword, '091'), (keyword, '092'), (keyword, '093'), (keyword, '094'),
                            (keyword, '095'), (keyword, '096'), (keyword, '097'), (keyword, '098'), (keyword, '099')
                            ])
        pool.close()
        pool.join()

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        print('Results 1')
        result1 = pool.map(search_dataframe,
                           [(keyword, '100'), (keyword, '101'), (keyword, '102'), (keyword, '103'), (keyword, '104'),
                            (keyword, '105'), (keyword, '106'), (keyword, '107'), (keyword, '108'), (keyword, '109'),
                            (keyword, '110'), (keyword, '111'), (keyword, '112'), (keyword, '113'), (keyword, '114'),
                            (keyword, '115'), (keyword, '116'), (keyword, '117'), (keyword, '118'), (keyword, '119'),
                            (keyword, '120'), (keyword, '121'), (keyword, '122'), (keyword, '123'), (keyword, '124'),
                            (keyword, '125'), (keyword, '126'), (keyword, '127'), (keyword, '128'), (keyword, '129'),
                            (keyword, '130'), (keyword, '131'), (keyword, '132'), (keyword, '133'), (keyword, '134'),
                            (keyword, '135'), (keyword, '136'), (keyword, '137'), (keyword, '138'), (keyword, '139'),
                            (keyword, '140'), (keyword, '141'), (keyword, '142'), (keyword, '143'), (keyword, '144'),
                            (keyword, '145'), (keyword, '146'), (keyword, '147'), (keyword, '148'), (keyword, '149'),
                            (keyword, '150'), (keyword, '151'), (keyword, '152'), (keyword, '153'), (keyword, '154'),
                            (keyword, '155'), (keyword, '156'), (keyword, '157'), (keyword, '158'), (keyword, '159'),
                            (keyword, '160'), (keyword, '161'), (keyword, '162'), (keyword, '163'), (keyword, '164'),
                            (keyword, '165'), (keyword, '166'), (keyword, '167'), (keyword, '168'), (keyword, '169'),
                            (keyword, '170'), (keyword, '171'), (keyword, '172'), (keyword, '173'), (keyword, '174'),
                            (keyword, '175'), (keyword, '176'), (keyword, '177'), (keyword, '178'), (keyword, '179'),
                            (keyword, '180'), (keyword, '181'), (keyword, '182'), (keyword, '183'), (keyword, '184'),
                            (keyword, '185'), (keyword, '186'), (keyword, '187'), (keyword, '188'), (keyword, '189'),
                            (keyword, '190'), (keyword, '191'), (keyword, '192'), (keyword, '193'), (keyword, '194'),
                            (keyword, '195'), (keyword, '196'), (keyword, '197'), (keyword, '198'), (keyword, '199')
                            ])
        pool.close()
        pool.join()

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        print('Results 2')
        result2 = pool.map(search_dataframe,
                           [(keyword, '200'), (keyword, '201'), (keyword, '202'), (keyword, '203'), (keyword, '204'),
                            (keyword, '205'), (keyword, '206'), (keyword, '207'), (keyword, '208'), (keyword, '209'),
                            (keyword, '210'), (keyword, '211'), (keyword, '212'), (keyword, '213'), (keyword, '214'),
                            (keyword, '215'), (keyword, '216'), (keyword, '217'), (keyword, '218'), (keyword, '219'),
                            (keyword, '220'), (keyword, '221'), (keyword, '222'), (keyword, '223'), (keyword, '224'),
                            (keyword, '225'), (keyword, '226'), (keyword, '227'), (keyword, '228'), (keyword, '229'),
                            (keyword, '230'), (keyword, '231'), (keyword, '232'), (keyword, '233'), (keyword, '234'),
                            (keyword, '235'), (keyword, '236'), (keyword, '237'), (keyword, '238'), (keyword, '239'),
                            (keyword, '240'), (keyword, '241'), (keyword, '242'), (keyword, '243'), (keyword, '244'),
                            (keyword, '245'), (keyword, '246'), (keyword, '247'), (keyword, '248'), (keyword, '249'),
                            (keyword, '250'), (keyword, '251'), (keyword, '252'), (keyword, '253'), (keyword, '254'),
                            (keyword, '255'), (keyword, '256'), (keyword, '257'), (keyword, '258'), (keyword, '259'),
                            (keyword, '260'), (keyword, '261'), (keyword, '262'), (keyword, '263'), (keyword, '264'),
                            (keyword, '265'), (keyword, '266'), (keyword, '267'), (keyword, '268'), (keyword, '269'),
                            (keyword, '270'), (keyword, '271'), (keyword, '272'), (keyword, '273'), (keyword, '274'),
                            (keyword, '275'), (keyword, '276'), (keyword, '277'), (keyword, '278'), (keyword, '279'),
                            (keyword, '280'), (keyword, '281'), (keyword, '282'), (keyword, '283'), (keyword, '284'),
                            (keyword, '285'), (keyword, '286'), (keyword, '287'), (keyword, '288'), (keyword, '289'),
                            (keyword, '290'), (keyword, '291'), (keyword, '292'), (keyword, '293'), (keyword, '294'),
                            (keyword, '295'), (keyword, '296'), (keyword, '297'), (keyword, '298'), (keyword, '299')
                            ])
        pool.close()
        pool.join()

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        print('Results 3')
        result3 = pool.map(search_dataframe,
                           [(keyword, '300'), (keyword, '301'), (keyword, '302'), (keyword, '303'), (keyword, '304'),
                            (keyword, '305'), (keyword, '306'), (keyword, '307'), (keyword, '308'), (keyword, '309'),
                            (keyword, '310'), (keyword, '311'), (keyword, '312'), (keyword, '313'), (keyword, '314'),
                            (keyword, '315'), (keyword, '316'), (keyword, '317'), (keyword, '318'), (keyword, '319'),
                            (keyword, '320'), (keyword, '321'), (keyword, '322'), (keyword, '323'), (keyword, '324'),
                            (keyword, '325'), (keyword, '326'), (keyword, '327'), (keyword, '328'), (keyword, '329'),
                            (keyword, '330'), (keyword, '331'), (keyword, '332'), (keyword, '333'), (keyword, '334'),
                            (keyword, '335'), (keyword, '336'), (keyword, '337'), (keyword, '338'), (keyword, '339'),
                            (keyword, '340'), (keyword, '341'), (keyword, '342'), (keyword, '343'), (keyword, '344'),
                            (keyword, '345'), (keyword, '346'), (keyword, '347'), (keyword, '348'), (keyword, '349'),
                            (keyword, '350'), (keyword, '351'), (keyword, '352'), (keyword, '353'), (keyword, '354'),
                            (keyword, '355'), (keyword, '356'), (keyword, '357'), (keyword, '358'), (keyword, '359'),
                            (keyword, '360'), (keyword, '361'), (keyword, '362'), (keyword, '363'), (keyword, '364'),
                            (keyword, '365'), (keyword, '366'), (keyword, '367'), (keyword, '368'), (keyword, '369'),
                            (keyword, '370'), (keyword, '371'), (keyword, '372'), (keyword, '373'), (keyword, '374'),
                            (keyword, '375'), (keyword, '376'), (keyword, '377'), (keyword, '378'), (keyword, '379'),
                            (keyword, '380'), (keyword, '381'), (keyword, '382'), (keyword, '383'), (keyword, '384'),
                            (keyword, '385'), (keyword, '386'), (keyword, '387'), (keyword, '388'), (keyword, '389'),
                            (keyword, '390'), (keyword, '391'), (keyword, '392'), (keyword, '393'), (keyword, '394'),
                            (keyword, '395'), (keyword, '396'), (keyword, '397'), (keyword, '398'), (keyword, '399')
                            ])
        pool.close()
        pool.join()

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        print('Results 4')
        result4 = pool.map(search_dataframe,
                           [(keyword, '400'), (keyword, '401'), (keyword, '402'), (keyword, '403'), (keyword, '404'),
                            (keyword, '405'), (keyword, '406'), (keyword, '407'), (keyword, '408'), (keyword, '409'),
                            (keyword, '410'), (keyword, '411'), (keyword, '412'), (keyword, '413'), (keyword, '414'),
                            (keyword, '415'), (keyword, '416'), (keyword, '417'), (keyword, '418'), (keyword, '419'),
                            (keyword, '420'), (keyword, '421'), (keyword, '422'), (keyword, '423'), (keyword, '424'),
                            (keyword, '425'), (keyword, '426'), (keyword, '427'), (keyword, '428'), (keyword, '429'),
                            (keyword, '430'), (keyword, '431'), (keyword, '432'), (keyword, '433'), (keyword, '434'),
                            (keyword, '435'), (keyword, '436'), (keyword, '437'), (keyword, '438'), (keyword, '439'),
                            (keyword, '440'), (keyword, '441'), (keyword, '442'), (keyword, '443'), (keyword, '444'),
                            (keyword, '445'), (keyword, '446'), (keyword, '447'), (keyword, '448'), (keyword, '449'),
                            (keyword, '450'), (keyword, '451'), (keyword, '452'), (keyword, '453'), (keyword, '454'),
                            (keyword, '455'), (keyword, '456'), (keyword, '457'), (keyword, '458'), (keyword, '459'),
                            (keyword, '460'), (keyword, '461'), (keyword, '462'), (keyword, '463'), (keyword, '464'),
                            (keyword, '465'), (keyword, '466'), (keyword, '467'), (keyword, '468'), (keyword, '469'),
                            (keyword, '470'), (keyword, '471'), (keyword, '472'), (keyword, '473'), (keyword, '474'),
                            (keyword, '475'), (keyword, '476'), (keyword, '477'), (keyword, '478'), (keyword, '479'),
                            (keyword, '480'), (keyword, '481'), (keyword, '482'), (keyword, '483'), (keyword, '484'),
                            (keyword, '485'), (keyword, '486'), (keyword, '487'), (keyword, '488'), (keyword, '489'),
                            (keyword, '490'), (keyword, '491'), (keyword, '492'), (keyword, '493'), (keyword, '494'),
                            (keyword, '495'), (keyword, '496'), (keyword, '497'), (keyword, '498'), (keyword, '499')
                            ])
        pool.close()
        pool.join()

        pool = mp.Pool(processes=(mp.cpu_count() - 1))

        print('Results 5')
        result5 = pool.map(search_dataframe,
                           [(keyword, '500'), (keyword, '501'), (keyword, '502'), (keyword, '503'), (keyword, '504'),
                            (keyword, '505'), (keyword, '506'), (keyword, '507'), (keyword, '508'), (keyword, '509'),
                            (keyword, '510'), (keyword, '511'), (keyword, '512'), (keyword, '513'), (keyword, '514'),
                            (keyword, '515'), (keyword, '516'), (keyword, '517'), (keyword, '518'), (keyword, '519'),
                            (keyword, '520'), (keyword, '521'), (keyword, '522'), (keyword, '523'), (keyword, '524'),
                            (keyword, '525'), (keyword, '526'), (keyword, '527'), (keyword, '528'), (keyword, '529'),
                            (keyword, '530'), (keyword, '531'), (keyword, '532'), (keyword, '533'), (keyword, '534'),
                            (keyword, '535'), (keyword, '536'), (keyword, '537'), (keyword, '538'), (keyword, '539'),
                            (keyword, '540'), (keyword, '541'), (keyword, '542'), (keyword, '543'), (keyword, '544'),
                            (keyword, '545'), (keyword, '546'), (keyword, '547'), (keyword, '548'), (keyword, '549'),
                            (keyword, '550'), (keyword, '551'), (keyword, '552'), (keyword, '553'), (keyword, '554'),
                            (keyword, '555'), (keyword, '556'), (keyword, '557'), (keyword, '558'), (keyword, '559'),
                            (keyword, '560'), (keyword, '561'), (keyword, '562'), (keyword, '563'), (keyword, '564'),
                            (keyword, '565'), (keyword, '566'), (keyword, '567'), (keyword, '568'), (keyword, '569'),
                            (keyword, '570'), (keyword, '571'), (keyword, '572'), (keyword, '573'), (keyword, '574'),
                            (keyword, '575'), (keyword, '576'), (keyword, '577'), (keyword, '578'), (keyword, '579'),
                            (keyword, '580'), (keyword, '581'), (keyword, '582'), (keyword, '583'), (keyword, '584'),
                            (keyword, '585'), (keyword, '586'), (keyword, '587'), (keyword, '588'), (keyword, '589'),
                            (keyword, '590'), (keyword, '591'), (keyword, '592'), (keyword, '593'), (keyword, '594'),
                            (keyword, '595'), (keyword, '596'), (keyword, '597'), (keyword, '598'), (keyword, '599')
                            ])
        pool.close()
        pool.join()

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        print('Results 6')
        result6 = pool.map(search_dataframe,
                           [(keyword, '600'), (keyword, '601'), (keyword, '602'), (keyword, '603'), (keyword, '604'),
                            (keyword, '605'), (keyword, '606'), (keyword, '607'), (keyword, '608'), (keyword, '609'),
                            (keyword, '610'), (keyword, '611'), (keyword, '612'), (keyword, '613'), (keyword, '614'),
                            (keyword, '615'), (keyword, '616'), (keyword, '617'), (keyword, '618'), (keyword, '619'),
                            (keyword, '620'), (keyword, '621'), (keyword, '622'), (keyword, '623'), (keyword, '624'),
                            (keyword, '625'), (keyword, '626'), (keyword, '627'), (keyword, '628'), (keyword, '629'),
                            (keyword, '630'), (keyword, '631'), (keyword, '632'), (keyword, '633'), (keyword, '634'),
                            (keyword, '635'), (keyword, '636'), (keyword, '637'), (keyword, '638'), (keyword, '639'),
                            (keyword, '640'), (keyword, '641'), (keyword, '642'), (keyword, '643'), (keyword, '644'),
                            (keyword, '645'), (keyword, '646'), (keyword, '647'), (keyword, '648'), (keyword, '649'),
                            (keyword, '650'), (keyword, '651'), (keyword, '652'), (keyword, '653'), (keyword, '654'),
                            (keyword, '655'), (keyword, '656'), (keyword, '657'), (keyword, '658'), (keyword, '659'),
                            (keyword, '660'), (keyword, '661'), (keyword, '662'), (keyword, '663'), (keyword, '664'),
                            (keyword, '665'), (keyword, '666'), (keyword, '667'), (keyword, '668'),
                            (keyword, '670'), (keyword, '671'), (keyword, '672'), (keyword, '673'), (keyword, '674'),
                            (keyword, '675'), (keyword, '676'), (keyword, '677'), (keyword, '678'), (keyword, '679'),
                            (keyword, '680'), (keyword, '681'), (keyword, '682'), (keyword, '683'), (keyword, '684'),
                            (keyword, '685'), (keyword, '686'), (keyword, '687'), (keyword, '688'), (keyword, '689'),
                            (keyword, '690'), (keyword, '691'), (keyword, '692'), (keyword, '693'), (keyword, '694'),
                            (keyword, '695'), (keyword, '696'), (keyword, '697'), (keyword, '698'), (keyword, '699')
                            ])
        pool.close()
        pool.join()

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        print('Results 7')
        result7 = pool.map(search_dataframe,
                           [(keyword, '700'), (keyword, '701'), (keyword, '702'), (keyword, '703'), (keyword, '704'),
                            (keyword, '705'), (keyword, '706'), (keyword, '707'), (keyword, '708'), (keyword, '709'),
                            (keyword, '710'), (keyword, '711'), (keyword, '712'), (keyword, '713'), (keyword, '714'),
                            (keyword, '715'), (keyword, '716'), (keyword, '717'), (keyword, '718'), (keyword, '719'),
                            (keyword, '720'), (keyword, '721'), (keyword, '722'), (keyword, '723'), (keyword, '724'),
                            (keyword, '725'), (keyword, '726'), (keyword, '727'), (keyword, '728'), (keyword, '729'),
                            (keyword, '730'), (keyword, '731'), (keyword, '732'), (keyword, '733'), (keyword, '734'),
                            (keyword, '735'), (keyword, '736'), (keyword, '737'), (keyword, '738'), (keyword, '739'),
                            (keyword, '740'), (keyword, '741'), (keyword, '742'), (keyword, '743'), (keyword, '744'),
                            (keyword, '745'), (keyword, '746'), (keyword, '747'), (keyword, '748'), (keyword, '749'),
                            (keyword, '750'), (keyword, '751'), (keyword, '752'), (keyword, '753'), (keyword, '754'),
                            (keyword, '755'), (keyword, '756'), (keyword, '757'), (keyword, '758'), (keyword, '759'),
                            (keyword, '760'), (keyword, '761'), (keyword, '762'), (keyword, '763'), (keyword, '764'),
                            (keyword, '765'), (keyword, '766'), (keyword, '767'), (keyword, '768'), (keyword, '769'),
                            (keyword, '770'), (keyword, '771'), (keyword, '772'), (keyword, '773'), (keyword, '774'),
                            (keyword, '775'), (keyword, '776'), (keyword, '777'), (keyword, '778'), (keyword, '779'),
                            (keyword, '780'), (keyword, '781'), (keyword, '782'), (keyword, '783'), (keyword, '784'),
                            (keyword, '785'), (keyword, '786'), (keyword, '787'), (keyword, '788'), (keyword, '789'),
                            (keyword, '790'), (keyword, '791'), (keyword, '792'), (keyword, '793'), (keyword, '794'),
                            (keyword, '795'), (keyword, '796'), (keyword, '797'), (keyword, '798'), (keyword, '799')
                            ])
        pool.close()
        pool.join()
        '''
        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        print('Results 8')
        result8 = pool.map(search_dataframe,
                           [(keyword, '800'), (keyword, '801'), (keyword, '802'), (keyword, '803'), (keyword, '804'),
                            (keyword, '805'), (keyword, '806'), (keyword, '807'), (keyword, '808'), (keyword, '809'),
                            (keyword, '810'), (keyword, '811'), (keyword, '813'), (keyword, '814'),
                            (keyword, '815'), (keyword, '816'), (keyword, '817'), (keyword, '818'), (keyword, '819'),
                            (keyword, '820'), (keyword, '821'), (keyword, '822'), (keyword, '823'), (keyword, '824'),
                            (keyword, '825'), (keyword, '826'), (keyword, '827'), (keyword, '828'), (keyword, '829'),
                            (keyword, '830'), (keyword, '831'), (keyword, '832'), (keyword, '833'), (keyword, '834'),
                            (keyword, '835'), (keyword, '836'), (keyword, '837'), (keyword, '838'), (keyword, '839'),
                            (keyword, '840'), (keyword, '841'), (keyword, '842'), (keyword, '843'), (keyword, '844'),
                            (keyword, '845'), (keyword, '846'), (keyword, '847'), (keyword, '848'), (keyword, '849'),
                            (keyword, '850'), (keyword, '851'), (keyword, '853'), (keyword, '854'),
                            (keyword, '855'), (keyword, '856'), (keyword, '857'), (keyword, '859'),
                            (keyword, '860'), (keyword, '861'), (keyword, '862'), (keyword, '863'), (keyword, '864'),
                            (keyword, '865'), (keyword, '866'), (keyword, '867'), (keyword, '868'), (keyword, '869'),
                            (keyword, '870'), (keyword, '871'), (keyword, '872'), (keyword, '873'), (keyword, '874'),
                            (keyword, '875'), (keyword, '876'), (keyword, '877'), (keyword, '878'), (keyword, '879'),
                            (keyword, '880'), (keyword, '881'), (keyword, '882'), (keyword, '883'), (keyword, '884'),
                            (keyword, '885'), (keyword, '886'), (keyword, '887'), (keyword, '888'), (keyword, '889'),
                            (keyword, '890'), (keyword, '891'), (keyword, '892'), (keyword, '893'), (keyword, '894'),
                            (keyword, '895'), (keyword, '896'), (keyword, '897'), (keyword, '898'), (keyword, '899')
                            ])
        pool.close()
        pool.join()

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        print('Results 9')
        result9 = pool.map(search_dataframe,
                           [(keyword, '900'), (keyword, '901'), (keyword, '902'), (keyword, '903'), (keyword, '904'),
                            (keyword, '905'), (keyword, '906'), (keyword, '907'), (keyword, '908'), (keyword, '909'),
                            (keyword, '910'), (keyword, '911'), (keyword, '912'), (keyword, '913'), (keyword, '914'),
                            (keyword, '915'), (keyword, '916'), (keyword, '917'), (keyword, '918'), (keyword, '919'),
                            (keyword, '920'), (keyword, '921'), (keyword, '922'), (keyword, '923'), (keyword, '924'),
                            (keyword, '925'), (keyword, '926'), (keyword, '927'), (keyword, '928'), (keyword, '929'),
                            (keyword, '930'), (keyword, '931'), (keyword, '932'), (keyword, '933'), (keyword, '934'),
                            (keyword, '935'), (keyword, '936'), (keyword, '937'), (keyword, '938'), (keyword, '939'),
                            (keyword, '940'), (keyword, '941'), (keyword, '942'), (keyword, '943'), (keyword, '944'),
                            (keyword, '945'), (keyword, '946'), (keyword, '947'), (keyword, '948'), (keyword, '949'),
                            (keyword, '950'), (keyword, '951'), (keyword, '952'), (keyword, '953'), (keyword, '954'),
                            (keyword, '955'), (keyword, '956'), (keyword, '957'), (keyword, '958'), (keyword, '959'),
                            (keyword, '960'), (keyword, '961'), (keyword, '962'), (keyword, '963'), (keyword, '964'),
                            (keyword, '965'), (keyword, '966'), (keyword, '967'), (keyword, '968'), (keyword, '969'),
                            (keyword, '970'), (keyword, '971'), (keyword, '972')
                            ])
        pool.close()
        pool.join()

        joined_result = pd.concat(result9+result8
                                  #+ result7+result6+result5
                                  #+ result0+result1+result2+result3+result4
        )
    else:
        result = pool.map(search_dataframe,
                          [(keyword, '970'), (keyword, '971'), (keyword, '972')
                           ])
        pool.close()
        pool.join()

        joined_result = pd.concat(result)

    joined_dict = read_dataframe(joined_result)

    # joined_dict = results[0]
    # for r in results[1:]:
    #     for key in r.keys():
    #         if key in joined_dict.keys():
    #             aff = joined_dict[key][0]
    #             papers = joined_dict[key][1]
    #             citations = joined_dict[key][2]
    #             joined_dict[key] = [aff, papers + r[key][1], citations + r[key][2]]
    #         else:
    #             joined_dict[key] = r[key]

    print('Time=', time.time() - start_time)
    df = pd.DataFrame.from_dict(joined_dict, orient='index', columns=['Affiliation', 'Publications', 'Citations'])

    df['Name'] = df.index
    print('Shape 1=', df.shape[0])
    # df['Z'] = [sum(x) for x in df['Citations']]
    df['Z'] = [len(x) for x in df['Publications']]
    df = df.sort_values(by=['Z'], ascending=False)
    df = df[['Name', 'Affiliation', 'Publications', 'Citations']]

    h_indices = []
    for c in df['Citations']:
        h = 0
        for i, p in enumerate(sorted(c, reverse=True)):
            if p > i:
                h += 1
        h_indices.append(h)

    df['Name'] = df['Name'].str.replace('-', '; ')
    df['Name'] = df['Name'].str.replace("'", '')
    df['Name'] = df['Name'].str.replace(',', ';')

    df['Index'] = h_indices
    # df = df.sort_values(by=['Index'], ascending=False)
    if max_res < 200:
        df = df[:max_res]
    else:
        df = df
    # df = df.drop('Citations', axis=1)
    if df.shape[0] == 0:
        return "<html><body><h1>Keyword not found!</h1><h1><button onclick='goBack()'>Go Back</button><script>function \
        goBack() {window.history.back();}</script></h1></body></html>"
    else:
        write_table(df)
        return render_template('key_results.html')
        # return string


@app.route('/nkresult/<list:argus>')
@login_required
def newkeysearch(argus):
    import time
    print(argus)
    keyword, max_res = argus
    max_res = int(max_res)
    start_time = time.time()

    pool = mp.Pool(processes=(mp.cpu_count() - 1))

    result = pool.map(search_new_dataframe,
                      [(keyword, '2018')
                       ])
    pool.close()
    pool.join()

    joined_result = pd.concat(result)

    joined_dict = read_new_dataframe(joined_result)

    print('Time=', time.time() - start_time)
    df = pd.DataFrame.from_dict(joined_dict, orient='index', columns=['Affiliation', 'Projects', 'Publications',
                                                                      'Total Costs', 'Clinical Studies', 'Patents'])

    df['Name'] = df.index
    df['Name'] = df['Name'].str.replace(';', '')
    df['Name'] = df['Name'].str.replace(',', ';')
    print('Shape 1=', df.shape[0])
    # df['Z'] = [sum(x) for x in df['Citations']]
    df['Z'] = [sum([float(y) for y in x if y != 'N/A']) for x in df['Total Costs']]
    df = df.sort_values(by=['Z'], ascending=False)
    df = df[['Name', 'Affiliation', 'Projects', 'Total Costs', 'Publications', 'Clinical Studies', 'Patents']]

    # h_indices = []
    # for c in df['Publications']:
    #     h = 0
    #     for i, p in enumerate(sorted(c, reverse=True)):
    #         if p > i:
    #             h += 1
    #     h_indices.append(h)

    df['Name'] = df['Name'].str.replace('-', ', ')
    # df['Index'] = h_indices
    # df = df.sort_values(by=['Index'], ascending=False)
    if max_res < 200:
        df = df[:max_res]
    else:
        df = df
    # df = df.drop('Citations', axis=1)
    if df.shape[0] == 0:
        return "<html><body><h1>Keyword not found!</h1><h1><button onclick='goBack()'>Go Back</button><script>function \
        goBack() {window.history.back();}</script></h1></body></html>"
    else:
        write_new_table(df)
        return render_template('new_key_results.html')
        # return string


@app.route('/cresult/<key>')
def cap_search(key):
    #print(argus)
    #fn, ln = argus

    # with open('authors_with_patents_9.json') as json_file:
    #     data = json.load(json_file)
    #with open('./author_files/authors_comb_9.json') as json_file:
    #    data = json.load(json_file)
    key = key.strip()
    name = key[0]
    print(key, name)
    with open('./author_files/authors_comb_' + name + '.pkl', 'rb') as f:
        data = pickle.load(f)

    # key = ln + '-' + fn
    if key not in data.keys():
        return "<html><body><h1>Keyword not found!</h1><h1><button onclick='goBack()'>Go Back</button><script>function \
        goBack() {window.history.back();}</script></h1></body></html>"
    else:
        print(data[key])
        write_html(key, data[key])
        return render_template('name_results.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        # fn = request.form['fn'].replace('/', ' ')
        # ln = request.form['ln'].replace('/', ' ')
        kw = request.form['kw']
        max_res = request.form['max_res']
        # return redirect(url_for('cap_search', argus=[fn, ln, max_res]))
        return redirect(url_for('keysearch', argus=[kw, max_res]))


@app.route('/newsearch', methods=['POST', 'GET'])
def newsearch():
    if request.method == 'POST':
        # fn = request.form['fn'].replace('/', ' ')
        # ln = request.form['ln'].replace('/', ' ')
        kw = request.form['kw']
        max_res = request.form['max_res']
        # return redirect(url_for('cap_search', argus=[fn, ln, max_res]))
        return redirect(url_for('newkeysearch', argus=[kw, max_res]))


@app.route('/name_search', methods=['POST', 'GET'])
def name_search():
    if request.method == 'POST':
        fn = request.form['fn'].replace('/', ' ')
        ln = request.form['ln'].replace('/', ' ')
        # kw = request.form['kw']
        key = ln + '-' + fn
        return redirect(url_for('cap_search', key=key))
        # return redirect(url_for('keysearch', argus=[kw, max_res]))


@app.route('/main_search')
@login_required
def main_search():
    return render_template('main_search.html')


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == password:
                login_user(user)
                return redirect(url_for('main_search'))
            else:
                return abort(401)
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            Username:<br>
            <p><input type=text name=username>
            <br>
            Password:<br>
            <p><input type=password name=password>
            <br><br>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


# handle login failed
@app.errorhandler(401)
def page_not_found():
    return render_template('login_failed.html')


# callback to reload the user object
@login_manager.user_loader
def load_user(username):
    user_entry = User.get(username)
    return User(user_entry[0], user_entry[1])


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSANOTHERSECRET"
    app.run(debug=True, port=5000)
