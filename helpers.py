from HTMLParser import HTMLParser

class ParseHTMLTags(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.counter = 0
        self.data_array = {}
        self.split_data = [0, 0]

    def handle_starttag(self, tag, attrs):
        #print "Start tag:", tag
        if tag == 'value':
            self.counter += 1
            self.data_array['value' + str(self.counter)] =  []
            self.data_array['value' + str(self.counter)].append(tag)
        
        if self.counter > 0:
            self.data_array['value' + str(self.counter)].append(tag)

    def handle_data(self, data):
        #print "Data:", data
        if self.counter > 0:
            self.data_array['value' + str(self.counter)].append(data)

    def split_data_for_row(self, away_team_id):
        for key, value in self.data_array.iteritems():
            try:
                j = value.index('team')
                if int(value[j + 1]) == away_team_id:
                    self.split_data[0] += 1
                else:
                    self.split_data[1] += 1
            except ValueError:
                'do nothing'

    def split_data_for_row2(self):
        #print(self.data_array)
        for key, value in self.data_array.iteritems():
            try:
                j = value.index('elapsed')
                if int(value[j + 1]) == 90:
                    i = value.index('awaypos')
                    k = value.index('homepos')
                    self.split_data[0] = int(value[i + 1])
                    self.split_data[1] = int(value[k + 1])

            except ValueError:
                'do nothing'


    # Getters
    def get_data_array(self):
        return self.data_array

    def get_split_data(self):
        return self.split_data
