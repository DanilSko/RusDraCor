import re
import transliterate
import os

for root, dirs, files in os.walk('./wikisource_raws/1_preprocessed/'):
    for file in files:
        if file.endswith('.txt'):
            print(file)
            text = open('./wikisource_raws/1_preprocessed/' + file, 'r', encoding='utf-8')
            text_read = text.read()
            text.close()
            text_read = text_read.split('</div>')[0]
            cast = re.findall('\{\| class=personae(.*?)'
                              '\|\}', text_read, re.DOTALL)
            castListLine = ''
            if len(cast) != 0:
                castItems = re.findall('\{\{razr2?\|(.*?)\}\}', cast[0])
                for person in castItems:
                    castListLine += '<castItem>' + person + '</castItem>\n'
            title = re.findall('НАЗВАНИЕ *?= ?(.*?)\n', text_read)
            if len(title) != 0:
                title = title[0]
            else: title = ''
            subtitle = re.findall('ПОДЗАГОЛОВОК *?= ?(.*?)\n', text_read)
            if len(subtitle) != 0:
                subtitle = subtitle[0]
            else: subtitle = ''
            author = re.findall('АВТОР *?= ?\[\[(.*?)\]\]', text_read)
            if len(author) != 0:
                author = author[0]
            else: author = ''
            creation_date = re.findall('ДАТАСОЗДАНИЯ *?= ?(.*?)\n', text_read)
            if len(creation_date) != 0:
                creation_date = creation_date[0]
            else: creation_date = ''
            print_date = re.findall('ДАТАПУБЛИКАЦИИ *?= ?(.*?)\n', text_read)
            if len(print_date) != 0:
                print_date = print_date[0]
            else: print_date = ''
            '''
            razrs = re.findall('\{\{Razr\|.*?\}\}', text_read)
            for el in razrs:
                e = re.findall('\{\{Razr\|(.*?)\}\}', el)[0]
                text_read = re.sub(el, '<actor>' + e + '</actor>', text_read)
            text = open('./wikisource_raws/1/' + file, 'w', encoding='utf-8')
            text.write(text_read)
            text.close()
            '''
            text = open('./wikisource_raws/1_preprocessed/' + file, 'r', encoding='utf-8')
            tei_header = open('tei_header.xml', 'r', encoding='utf-8').read()
            text_tei = open('./wikisource_tei/1/' + file.split('.txt')[0] + '.xml', 'w', encoding='utf-8')
            text_tei.write(tei_header)

            poem = False
            cast = False
            castList = []
            start = False
            sp = False
            for line in text:
                if line == "<div class='drama text'>\n":
                    start = True
                if start:
                    '''
                    if 'действующие лица' in line.lower():
                        cast = True
                    if cast:
                        if len(re.findall('\{\{razr2?\|(.*?)\}\}', line)) != 0:
                            castList.append(re.findall('\{\{razr2?\|(.*?)\}\}', line)[0])
                    '''
                    if line.startswith('{{rem') or line.startswith('{{Rem'):
                        stage = re.findall('\{\{[Rr]em2?\|(.*?)\}\} *\n', line)[0]
                        text_tei.write('<stage>' + stage + '</stage>\n')
                    if line == '\n' or line == '----\n':
                        pass

                    if line.startswith('<poem'):
                        poem = True
                    if line.startswith('</poem>'):
                        poem = False
                    if line.lower().startswith('{{re|'):
                        speaker = re.findall('\{\{[Rr]e\|(.*?)\|', line)
                        if len(speaker) == 0:
                            speaker = re.findall('\{\{[Rr]e\|(.*?)\}\}', line)
                            speaker = speaker[0]
                        else:
                            speaker = re.findall('\{\{[Rr]e\|(.*?)\|', line)[0]
                        speaker_id = transliterate.translit(speaker, 'ru', reversed=True)
                        speaker_id = re.sub("[ \.'<>]", '', speaker_id)
                        speaker_id = speaker_id.title()
                        stage_del = re.findall('\{\{[Rr]e\|' + speaker + '\|(\(.*?\))\}\}', line)
                        if len(stage_del) != 0 and len(speaker) != 0:
                            stage_del = stage_del[0]
                            text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>'
                                            + ' <stage type="delivery">' + stage_del
                                            + '</stage>\n')
                        if len(stage_del) == 0 and len(speaker) != 0:
                            text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>\n')
                        if len(stage_del) != 0 and len(speaker) == 0:
                            stage_del = stage_del[0]
                            text_tei.write('<stage>' + stage_del + '</stage>\n')
                    #if line == '\n':
                        #text_tei.write('</sp>\n')
                    if line.lower().startswith('{{реплика'):
                        # print(line)
                        speaker = re.findall('\{\{[Рр]еплика\|(.*?)\|', line)
                        if len(speaker) == 0:
                            speaker = re.findall('\{\{[Рр]еплика\|(.*?)\}\}', line)
                            speaker = speaker[0]
                        else:
                            speaker = re.findall('\{\{[Рр]еплика\|(.*?)\|', line)[0]
                        speaker_id = transliterate.translit(speaker, 'ru', reversed=True)
                        speaker_id = speaker_id.title()
                        speaker_id = re.sub("[ \.'<>]", '', speaker_id)
                        # print('\{\{[Рр]еплика\|' + speaker + '\|(.*?)\}\}')
                        stage_del = re.findall('\{\{[Рр]еплика\|' + speaker + '\|(.*?)\}\}', line)
                        if len(stage_del) != 0 and len(speaker) != 0:
                            stage_del = stage_del[0]
                            # print(line)
                            # print(speaker)
                            # print(stage_del)
                            text_of_line = line.split(speaker + '|' + stage_del + '}} ')[1]
                            # print(text_of_line)
                            text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>'
                                            + ' <stage type="delivery">' + stage_del
                                            + '</stage>\n' + '<p>' + text_of_line + '</p>' + '\n')
                        if len(stage_del) == 0 and len(speaker) != 0:
                            text_of_line = line.split(speaker + '}} ')[1]
                            text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>\n'
                                            + '<p>' + text_of_line + '</p>' + '\n')
                    if line.startswith('<h3>'):
                        scene_title = re.findall('<h3>(.*?)</h3>', line)[0]
                        text_tei.write('<div type="act">\n<head>' + scene_title + '</head>\n')
                    if line.startswith('<h4>'):
                        scene_title = re.findall('<h4>(.*?)</h4>', line)[0]
                        text_tei.write('<div type="scene">\n<head>' + scene_title + '</head>\n')
                    if line.startswith('<center>'):
                        stage_text = re.findall('<center>(.*?)</center>', line)[0]
                        text_tei.write('<stage>' + stage_text + '</stage>\n')

                    if line.startswith('{{h2|'):
                        kartina = re.findall('\{\{h2\|(.*?)\}\}', line)[0]
                        text_tei.write('<div type="scene">\n<head>' + kartina + '</head>\n')
                    if line.startswith('=='):
                        if 'действие' in line.lower():
                            act = re.findall('\=\= (.*?) \=\=', line)[0]
                            text_tei.write('<div type="act">\n<head>' + act + '</head>\n')
                        elif 'явление' in line.lower():
                            scene = re.findall('\=\= (.*?) \=\=', line)[0]
                            text_tei.write('<div type="scene">\n<head>' + scene + '</head>\n')
                        elif 'сцена' in line.lower():
                            scene = re.findall('\=\= (.*?) \=\=', line)[0]
                            text_tei.write('<div type="scene">\n<head>' + scene + '</head>\n')
                        else:
                            other = re.findall('\=\= (.*?) \=\=', line)[0]
                            text_tei.write('<div type="other">\n<head>' + other + '</head>\n')
                    else:
                        if poem:
                            if not line.startswith('{{Re|') and not line.startswith('{{re|')\
                                    and not line.startswith('{{rem|') and not line.startswith('{{Rem|')\
                                    and not line.startswith('{{rem2|') and not line.startswith('{{Rem2|')\
                                    and not line.startswith('<h4>') and not line == '<poem>\n'\
                                    and not line.startswith('<h3>') and not line.startswith('<center>')\
                                    and not line.startswith('==') and not line.startswith('{{h2'):
                                if line == '----\n' or line == '<poem>\n':
                                    pass
                                if line == '\n':
                                    pass
                                else:
                                    if 'indent' in line:
                                        line = line.split('}}')[1]
                                        text_tei.write('<l part="F">' + line.split('\n')[0] + '</l>\n')
                                    else:
                                        text_tei.write('<l>' + line.split('\n')[0] + '</l>\n')
                        if not poem:
                            if not line.startswith('{{Re|') and not line.startswith('{{re|')\
                                    and not line.startswith('{{rem|') and not line.startswith('{{Rem|')\
                                    and not line.startswith('{{rem2|') and not line.startswith('{{Rem2|')\
                                    and not line.startswith('<h4>') and not line.startswith('|')\
                                    and not line.startswith('<h3>') and not line.startswith('<center>')\
                                    and not line == '</poem>\n' and not line.lower().startswith('{{реплика')\
                                    and not line.startswith('{{h2'):
                                '''
                                if line.lower().startswith('{{реплика|'):
                                    print(line)
                                    speaker = re.findall('\{\{Реплика\|(.*?)\|', line)
                                    if len(speaker) == 0:
                                        speaker = re.findall('\{\{Реплика\|(.*?)\}\}', line)[0]
                                    else:
                                        speaker = speaker[0]
                                    speaker_id = transliterate.translit(speaker, 'ru', reversed=True)
                                    stage_del = re.findall('\{\{Реплика\|' + speaker + '\|(.*?)\}\}', line)
                                    if len(stage_del) != 0 and len(speaker) != 0:
                                        stage_del = stage_del[0]
                                        text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>'
                                                        + '<stage type="delivery">' + stage_del
                                                        + '</stage>\n')
                                    if len(stage_del) == 0 and len(speaker) != 0:
                                        text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>\n')
                                '''

                                if line == '\n':
                                    pass
                                if line == "<div class='drama text'>\n":
                                    pass
                                if line.startswith('<center>'):
                                    pass
                                else:
                                    text_tei.write('<p>' + line.split('\n')[0] + '</p>\n')



            text_tei.write('</body>\n</text>\n</TEI>')

            text_tei.close()
            text_tei = open('./wikisource_tei/1/' + file.split('.txt')[0] + '.xml', 'r', encoding='utf-8')
            text_tei_read = text_tei.read()
            text_tei.close()
            text_tei_read = re.sub('<l></l>\n', '', text_tei_read)
            text_tei_read = re.sub('<p></p>\n', '', text_tei_read)
            text_tei_read = re.sub('<sp>', '</sp>\n<sp>', text_tei_read)
            text_tei_read = re.sub('<sp who', '</sp>\n<sp who', text_tei_read)
            text_tei_read = re.sub('<l></l>\n', '', text_tei_read)
            text_tei_read = re.sub('<p></p>\n', '', text_tei_read)
            text_tei_read = re.sub('</l>\n<div', '</l>\n</sp>\n<div', text_tei_read)
            text_tei_read = re.sub('</sp>\n<div', '</sp>\n</div>\n<div', text_tei_read)
            text_tei_read = re.sub('</stage>\n<div', '</stage>\n</div>\n<div', text_tei_read)
            text_tei_read = re.sub('</p>\n<div', '</p>\n</div>\n<div', text_tei_read)
            text_tei_read = re.sub("<p><div class='drama text'></p>\n", '', text_tei_read)
            text_tei_read = re.sub("<p>{\| class=personae</p>\n", '', text_tei_read)
            text_tei_read = re.sub('<ref.*?>.*?</ref>', '', text_tei_read)
            text_tei_read = re.sub('<div type="other">\n<head>Примечания</head>\n', '', text_tei_read)
            text_tei_read = re.sub('<p><h2>Пояснения:</h2></p>\n', '', text_tei_read)
            text_tei_read = re.sub('<p>\{\{примечания\}\}</p>\n', '', text_tei_read)
            text_tei_read = re.sub('<p>\{\{Примечания\}\}</p>\n', '', text_tei_read)
            text_tei_read = re.sub('<l><poem class=p1></l>\n', '', text_tei_read)
            text_tei_read = re.sub('<p></poem></p>\n', '', text_tei_read)
            text_tei_read = re.sub('<l><references /></l>\n', '', text_tei_read)
            text_tei_read = re.sub('<p></poem><poem class=p00></p>\n', '', text_tei_read)
            text_tei_read = re.sub('<l><poem class=p00></l>\n', '', text_tei_read)
            text_tei_read = re.sub('<l><poem class=p0></l>\n', '', text_tei_read)
            text_tei_read = re.sub('<stage><stage>', '<stage>', text_tei_read)
            text_tei_read = re.sub('</stage></stage>', '</stage>', text_tei_read)
            text_tei_read = re.sub('<l><br /></l>\n', '<lb/>\n', text_tei_read)
            text_tei_read = re.sub('<p><br /></p>\n', '<lb/>\n', text_tei_read)
            text_tei_read = re.sub('<author></author>', '<author>' + author + '</author>', text_tei_read)
            text_tei_read = re.sub('<title type="main"></title>', '<title type="main">' + title + '</title>', text_tei_read)
            text_tei_read = re.sub('<title type="sub"></title>', '<title type="sub">' + subtitle + '</title>', text_tei_read)
            text_tei_read = re.sub('<date type="written"></date>', '<date type="written">' + creation_date + '</date>', text_tei_read)
            text_tei_read = re.sub('<date type="print"></date>', '<date type="print">' + print_date + '</date>', text_tei_read)
            cursive_stages = re.findall("''.*?''", text_tei_read)
            for el in cursive_stages:
                e = re.findall("''(.*?)''", el)[0]
                text_tei_read = re.sub(re.escape(el), '<stage>' + e + '</stage>', text_tei_read)
            participants = set(re.findall('<speaker>(.*?)</speaker>', text_tei_read))
            particDescLine = '<particDesc>\n<listPerson>\n'
            for participant in participants:
                participant_tr = transliterate.translit(participant, 'ru', reversed=True)
                participant_tr = participant_tr.title()
                participant_tr = re.sub("[ \.'<>]", '', participant_tr)
                particDescLine += '<person xml:id="' + participant_tr + '">\n' +\
                                  '<persName>' + participant + '</persName>\n' + '</person>\n'
            text_tei_read = re.sub('<profileDesc>\n', '<profileDesc>\n' + particDescLine +
                                   '</listPerson>\n</particDesc>\n', text_tei_read)
            if castListLine is not '':
                text_tei_read = re.sub('<body>\n', '<body>\n<castList>\n<head>ДЕЙСТВУЮЩИЕ ЛИЦА</head>\n' +
                                       castListLine + '</castList>\n', text_tei_read)
            text_tei = open('./wikisource_tei/1/' + file.split('.txt')[0] + '.xml', 'w', encoding='utf-8')
            text_tei.write(text_tei_read)