# file: voter_analytics/views.py
# author: Cody Headings, codyh@bu.edu, 10/30/2025
# desc: view functions to return html renders

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter

# Create your views here.
class VoterListView(ListView):
    '''View to display voter info'''
 
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        """Limit the queryset."""
        # start with entire queryset
        results = super().get_queryset().order_by('precinct')

        # filter results by these field(s):
        
                
        return results