#coding:utf-8
import requests
import string

class ConGraphAPI:
    '''
    For details, refer to: https://concept.research.microsoft.com/Home/API
    Get score of concepts per instance
    '''
    TYPE_DICT = {'p_ce':'ScoreByProb',
                 'MI':'ScoreByMI',
                 'p_ec':'ScoreByTypi',
                 'NPMI':'ScoreByNPMI',
                 'PMIK':'ScoreByPMIK',
                 'BLC':'ScoreByCross'}

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://concept.research.microsoft.com/api/Concept/'
        self.instance_buffer = {}


    def clear_buffer(self):
        # Remember to clear buffer if arguments changed.
        self.instance_buffer = {}

    def getScore(self, instance, type='p_ce', topK=10, pmiK=10, smooth=0):
        '''
        Get concept score
        See https://concept.research.microsoft.com/help/ for details
        :param type: one of {'p_ce', 'MI', 'p_ec', 'NMPI', 'PMIK', 'BLC'}
        :param topK:
        :param pmiK:
        :param smooth:
        :return:
        '''
        if not self.TYPE_DICT.has_key(type):
            raise Exception('msg', 'No such type: '+type)
        if self.instance_buffer.has_key(instance):
            print 'Caught in buffer :)'
            instance_score = self.instance_buffer[instance]
        else:
            request_url = self.base_url + self.TYPE_DICT[type]
            param = {'instance': instance,
                 'topK': topK,
                 'api_key': self.api_key}
            if type != 'p_ce':
                param['smooth'] = smooth
            if type == 'PMIK' or type == 'BLC':
                param['pmiK'] = pmiK
            req = requests.get(request_url, param)
            # print req.content
            instance_score = req.json()
            self.instance_buffer[instance] = instance_score
        print 'Q > ' + instance
        return instance_score

    def getConceptScoreList(self, sentence, type='p_ce', topK=10, pmiK=10, smooth=0):
        '''

        :param sentence:
        :param type:
        :param topK:
        :param pmiK:
        :param smooth:
        :return: a dictionary of {'concept':[score0, score1, ...], ...}
        '''
        # Remove punctuation in string
        sentence = sentence.translate(string.maketrans("",""), string.punctuation)
        sentence = sentence.split()
        cum_dict = {}
        for word in sentence:
            word_dict = self.getScore(word, type, topK, pmiK, smooth)
            for concept, score in word_dict.iteritems():
                if cum_dict.has_key(concept):
                    cum_dict[concept].append(score)
                else:
                    cum_dict[concept] = [score]
        return cum_dict

    def getConceptScoreListSum(self, conceptScoreList):
        results = {}
        for concept, scoreList in conceptScoreList.iteritems():
            results[concept] = sum(scoreList)
        return results



if __name__=='__main__':
    cgAPI = ConGraphAPI('8jKN8BcdzZ6tQxTnv4ONbtNCXVbFtBAh')
    ret_json = cgAPI.getScore('belt', type='BLC')
    print ret_json
    sentence = "think good way combine these two items have full torso-sized back straightener belt like second diagram, like first diagram, insert magnets stick chair-mounted magnetic strip. help user posture idea add incentive using device device strapped person attached chair powered massage rollers massage  user correcting posture same time massage rollers heat vibration setting feel people more apt using device incentive  getting massage. "
    concept_score_list = cgAPI.getConceptScoreList(sentence, type='BLC', topK=5)
    #print concept_score_list
    sum_score_list = cgAPI.getConceptScoreListSum(concept_score_list)
    print sum_score_list