# file: voter_analytics/views.py
# author: Cody Headings, codyh@bu.edu, 10/30/2025
# desc: view functions to return html renders

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
from datetime import date

# Create your views here.
class VoterListView(ListView):
    '''View to display list of voter info'''
 
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        """Limit the queryset."""
        # start with entire queryset
        voters = super().get_queryset().order_by('dob')

        # filter results by these field(s):
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                voters = voters.filter(party=party)
        
        if 'vscore' in self.request.GET:
            voter_score = self.request.GET['vscore']
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state:
                voters = voters.filter(v20state=v20state)

        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town:
                voters = voters.filter(v21town=v21town)

        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary:
                voters = voters.filter(v21primary=v21primary)

        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general:
                voters = voters.filter(v22general=v22general)

        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town:
                voters = voters.filter(v23town=v23town)

        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                voters = voters.filter(dob__gte=date(int(min_dob),1,1))

        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                voters = voters.filter(dob__lte=date(int(max_dob),12,31))
                
        return voters

class VoterDetailView(DetailView):
    """View to display a single voter record."""

    template_name = "voter_analytics/voter.html"
    model = Voter
    context_object_name = "voter"