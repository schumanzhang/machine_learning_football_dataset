from HTMLParser import HTMLParser

class ParseShotOn(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.data_array = []
        self.split_data = {'away_team_shots_blocked': 0, 'home_team_shots_blocked': 0, 'away_team_shots_on_target': 0, 'home_team_shots_on_target': 0}

    def handle_starttag(self, tag, attrs):
        #print "Start tag:", tag
        self.data_array.append(tag)

    def handle_data(self, data):
        #print "Data:", data
        self.data_array.append(data)

    def split_data_for_row(self, away_team_id):
        self.data_array.pop(0)
        for index, item in enumerate(self.data_array):
            if item == 'value' and self.data_array[index + 2] == 'blocked':
                if int(self.data_array[index + 15]) == away_team_id:
                    self.split_data['away_team_shots_blocked'] += 1
                else:
                    self.split_data['home_team_shots_blocked'] += 1

            if item == 'value' and self.data_array[index + 2] == 'shoton':
                if int(self.data_array[index + 15]) == away_team_id:
                    self.split_data['away_team_shots_on_target'] += 1
                else:
                    self.split_data['home_team_shots_on_target'] += 1
                    
    # Getters
    def get_data_array(self):
        return self.data_array

    def get_split_data(self):
        return self.split_data
