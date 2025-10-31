# file: voter_analytics/models.py
# author: Cody Headings, codyh@bu.edu, 10/30/2025
# desc: definitions for data models

from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter from Newton.
    Name, address details, DOB, etc.
    '''
    # identification
    first_name = models.TextField()
    last_name = models.TextField()
    address_number = models.TextField()
    address_street = models.TextField()
    address_apt_number = models.TextField()
    address_zip = models.TextField()
    dob = models.DateTimeField()
    date_registered = models.DateTimeField()
    party = models.CharField(max_length=2)
    precinct = models.TextField()

    # voting info
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    voter_score = models.IntegerField()
 
    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}: {self.address_number} {self.address_street}, {self.party}'
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()

    filename = 'C:/Users/green/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
 
    for line in f:
        fields = line.split(',')

        # create a new instance of Voter object with this record from CSV
        try:
            voter = Voter(last_name=fields[1],
                            first_name=fields[2],
                            address_number = fields[3],
                            address_street = fields[4],
                            address_apt_number = fields[5],
                            address_zip = fields[6],
                            dob = fields[7],
                            date_registered =fields[8],
                            party = fields[9],
                            precinct = fields[10],
                            v20state = fields[11],
                            v21town = fields[12],
                            v21primary = fields[13],
                            v22general =fields[14],
                            v23town = fields[15],
                            voter_score = fields[16]
                        )
            voter.save() # commit to database
            print(f'Created voter: {voter}')
        except:
            print(f"Skipped: {fields}")

    print(f'Done. Created {len(Voter.objects.all())} Voters.')