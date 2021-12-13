#needed libs
import numpy as np
import pandas as pd
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import json


class Fuzzy:

    def __init__(self):
        #script config 
        DEBUG=True
        FILE='./data.csv'

        # DATA PRE-PROCESSING, USER CONFIGURATION
        #Definitions
        self.linguistic_terms = {
            'goodness' : ["very poor", "poor", "moderate", "good", "very good"],
            'agreement' : ["strongly disagree", "disagree", "neither agree nor disagree", "agree", "strongly agree"],
            'quantity' : ["very few", "a few", "moderate", "some", "very much"],
            'difficulty' : ["very difficult", "difficult", "moderate", "easy", "very easy"],
            'difficulty' : ["very difficult", "difficult", "moderate", "easy", "very easy"],
            'satisfaction' : ["very satisfied", "satisfied", "neither", "dissatisfied", "very dissatisfied"]
        }

        # fuzzify the following and map the linguistic terms
        # [ column_name : linguistic_terms_type, ...]
        self.columns_to_fuzzify = {
            'language_professor' : 'goodness',
            'quality_language_lectures' : 'goodness',
            'language_assistant' : 'goodness',
            'quality_language_exercises' : 'goodness',
            'content_is_understandable' : 'agreement',
            'examples' : 'agreement',
            'difficulty_lectures' : 'difficulty',
            'difficulty_exercices' : 'difficulty',
            'listening_professor' : 'goodness',
            'responsiveness_professor' : 'goodness',
            'responsiveness_assistant' : 'goodness',
            'course_structure' : 'agreement',
            'course_independently' : 'agreement',
            'course_evaluation_modalities' : 'agreement',
            'course_activities' : 'agreement',
            'expectations_lectures' : 'agreement',
            'course_prepared_exam' : 'agreement',
            'effort_lectures' : 'quantity',
            'effort_exercises' : 'quantity',
            'effort_exam_preperation' : 'quantity',
            'exam_difficulty' : 'difficulty',
            'statisfaction' : 'satisfaction'
        }


        # compute mean of the following columns
        columns_to_compute_mean = ["language_professor","quality_language_lectures","language_assistant","quality_language_exercises","content_is_understandable","examples","difficulty_lectures","difficulty_exercices","listening_professor","responsiveness_professor","responsiveness_assistant","course_structure","course_independently","course_evaluation_modalities","course_activities","expectations_lectures","course_prepared_exam","effort_lectures","effort_exercises","effort_exam_preperation","exam_difficulty","grading","statisfaction"]

        # group by what for mean?
        group_by = 'course_id'

        # other functions (split tracks and yes/no =>1/0) to be applied to the following columns
        crispify_binary = lambda x: 1 if x == 'yes' else 0
        # { column_name : fct_to_be_applied, ...}
        columns_other_fcts = {
            'course_category' : lambda x: x.split(","),
            'exercices_mandatory': crispify_binary,
            'open_book_exam': crispify_binary
        }

        # aggregate the following columns 
        # { aggregated_column_name : { list: [column_name_1, ..., column_name_n], weights : [w_1,...,w_n] }, ... }
        self.columns_to_aggregate = {
            'language_lecture' : { 'type': 'goodness', 'list' : ['language_professor', 'quality_language_lectures'], 'weights' : None },
            'language_exercises' : { 'type': 'goodness', 'list' : ['language_assistant', 'quality_language_exercises'], 'weights' : None },
            'understandability' : { 'type': 'goodness', 'list' : ['content_is_understandable', 'examples'], 'weights' : None },
            'difficulty' : { 'type': 'quantity', 'list' : ['difficulty_lectures', 'difficulty_exercices'], 'weights' : None },
            'commitment' : {  'type': 'goodness', 'list' : ['listening_professor','responsiveness_professor','responsiveness_assistant'], 'weights' : None },
            'quality' : { 'type': 'goodness', 'list' : ['course_structure','course_independently','course_evaluation_modalities', 'course_activities', 'expectations_lectures', 'course_prepared_exam'], 'weights' : None },
            'effort' : { 'type': 'quantity', 'list' : ['effort_lectures','effort_exercises','effort_exam_preperation'], 'weights' : None },
        }

        self.trapezoid_config = { 'low' : 0, 'high' : 4.5, 'padding' : 0.5 }

        #read from file
        df = pd.read_csv(FILE)

        #other fcts to be applied: split tracks and yes/no =>1/0
        for col in columns_other_fcts:
            fct = columns_other_fcts[col]
            df[col] = df[col].apply(fct)


        #fuzzify data 
        for col in self.columns_to_fuzzify:
            #get
            linguistics_type = self.columns_to_fuzzify[col]
            #of that column to fuzzify
            
            #now get
            ling_terms = self.linguistic_terms[linguistics_type]
            #for that specific column, e.g. very poor ... very good
            
            #define
            trapezoids = self.equal_trapezoids_fcts(ling_terms)
            #membership functions for that column
            
            #and finally apply the fct on the column, such that the linguistic terms 
            # get mapped to their preimage
            fuziffier = lambda x : self.term2fuzzynumber(x, trapezoids)
            
            df[col] =  df[col].apply(fuziffier)

            

        
        #compute means for the labels defined above and groupby
        means = {}
        for column in columns_to_compute_mean:
            means.setdefault(column, df.groupby(by=group_by)[column].mean())

        means = pd.DataFrame(means)
        dropped = df.drop(columns=columns_to_compute_mean).drop_duplicates(subset=[group_by])
        df = dropped.merge(means, how='outer', on=group_by)

        #aggregate columns, they're added as new columns to the pd frame
        for col in self.columns_to_aggregate:
            val = self.columns_to_aggregate[col]
            df[col] = self.aggregate(val['list'], df, weights=val['weights'])

        self.df = df


    def process_user_input(self,user_input):
        score_column = self.df.apply(lambda row : self.compute_score(row, user_input), axis = 1)

        self.df['score'] = score_column

        # prepare POST answer, i.e. convert fuzzy numbers back to terms
        strip_down = pd.DataFrame({})
        strip_down['course_name'] = self.df['course_name']
        strip_down['score'] = self.df['score']

        #defuzzify data
        for col in [*self.columns_to_aggregate]:
            
            #get
            linguistics_type = self.columns_to_aggregate[col]['type']
            #of that column to defuzzify
            
            #now get
            ling_terms = self.linguistic_terms[linguistics_type]
            #for that specific column, e.g. very poor ... very good
            
            #define
            trapezoids = self.equal_trapezoids_fcts(ling_terms)
            #membership functions for that column
            
            #and 
            fuzzynumber2term = lambda x : self.crisp2term(self.fuzzynumber2crisp(x, self.trapezoid_config['low'],self.trapezoid_config['high']), trapezoids)
            strip_down[col] =  self.df[col].apply(fuzzynumber2term)


        #additional data
        strip_down['exo'] = self.df['exercices_mandatory']
        strip_down['course_language'] = self.df['course_language']

        strip_down = strip_down.sort_values('score', ascending=False)

        result = strip_down.to_json(orient="split")
        parsed = json.loads(result)
        print(parsed)
        f=json.dumps(parsed, indent=4, sort_keys=False)
        print(f)
        return f

    # fuzzy converters
    # linguistic term -> fuzzy number, e.g. good -> [1.5, ... , 3]
    def term2fuzzynumber(self,term, trapezoids): 
        DEBUG=False
        return trapezoids[term]


    # crisp -> linguistic term, e.g .2 -> poor
    def crisp2term(self,val, trapezoids):
        DEBUG=False
        
        n = len(trapezoids)
            
        trapezoids_bp = [*trapezoids.values()]
        ling_terms= [*trapezoids]
        
        if DEBUG: print("Trapezoid functions (breaking points): ", trapezoids_bp)
        
        low = np.amin(trapezoids_bp)
        high = np.amax(trapezoids_bp)
        assert val <=high and val >= low
        x = np.arange(low, high+0.01, 0.1)
        
        memb_fcts = [ fuzz.trapmf(x, trapezoids_bp[i]) for i in range(0, n) ]
        evals = [ fuzz.interp_membership(x, memb_fcts[i], val) for i in range(0, n) ]

        if DEBUG:
            for i in range(0, n):
                print(i,"# evaluation:",ling_terms[i],evals[i])
        
        max_eval = max(evals)
        max_index = evals.index(max_eval)
        
        return ling_terms[max_index]
        

        
    # fuzzy number -> crisp 
    def fuzzynumber2crisp(self,memb_fct_, low, high):
        x = np.arange(low, high+0.01, 0.1)
        memb_fct = fuzz.trapmf(x, memb_fct_)
        
        # choose one of the following methods to defuzzify
        defuzzified = fuzz.defuzz(x, memb_fct, 'centroid')  # Same as skfuzzy.centroid
        # defuzzified = fuzz.defuzz(x, memb_fct, 'bisector')
        # defuzzified = fuzz.defuzz(x, memb_fct, 'mom')
        # defuzzified = fuzz.defuzz(x, memb_fct, 'som')
        # defuzzified = fuzz.defuzz(x, memb_fct, 'lom')
        return defuzzified

    def equal_trapezoids_fcts(self,linguistic_terms):
        DEBUG=False
        low=self.trapezoid_config['low']
        high=self.trapezoid_config['high']
        padding=self.trapezoid_config['padding']
        
        fcts = {}
        n = len(linguistic_terms)
        
        x = np.arange(low, high+0.01, 0.1)
        
        width_per_trape = (high-low+padding)/n
        
        #first,i=1 (edgcase)
        b = [0]*4
        b[0] = 0
        b[1] = 0
        b[2] = width_per_trape/2
        b[3] = width_per_trape
        v1 = np.array([b[0],b[1],b[2],b[3]])
        fcts.setdefault(linguistic_terms[0], v1)
        
        #vi, i=2,...,n-1
        for i in range(1,n-1):
            b[0] = b[2]
            b[1] = b[3]
            b[2] = b[2]+width_per_trape
            b[3] = b[3]+width_per_trape
            vi = np.array([b[0],b[1],b[2],b[3]])
            fcts.setdefault(linguistic_terms[i], vi)

        
        #last i=n (edgcase)
        b[0] = b[2]
        b[1] = b[3]
        b[2] = b[2]+width_per_trape
        b[3] = b[3]+width_per_trape/2
        vn = np.array([b[0],b[1],b[2],b[3]])
        fcts.setdefault(linguistic_terms[n-1], vn)
        
        if DEBUG: print(fcts)
        
        return fcts

    #compute score
    def compute_score(self,row, user_input):
        sum = 0
        
        # compute score regarding importance of 
        importance_attributes = [*self.columns_to_aggregate]
        
        for attribute in importance_attributes:
            if user_input[attribute] is not None:
                sum += self.fuzzynumber2crisp(row[attribute], self.trapezoid_config['low'], self.trapezoid_config['high'])*user_input[attribute]
        
        # delta kronecker+
        intersect = lambda i,j : bool(set(i) & set(j))
        
        #if course not in desired tracks
        if not intersect(row['course_category'], user_input['tracks']): 
            sum = 0
            
        #if mandatory exercises and user not ok with it
        if row['exercices_mandatory'] and not user_input['exercices_mandatory_ok']:
            sum = 0
        
        #if course given in prferred language
        if row['course_language'] not in user_input['preferred_lang']:
            sum = 0
        
        return sum

    # aggregate the columns defined in l_ (normal list) of the frame with the given weights
    def aggregate(self, l_, frame, weights=None, normalize=True):
        l = [ frame[col] for col in l_]
        
        if weights == None: 
            weights = np.array([1/len(l_)]*len(l_))
        elif normalize == True:
            weights = [ w/sum(weights) for w in weights ]
        
        return sum([ w*f for (w,f) in zip(weights,l)])





if __name__ == "__main__":
    main()