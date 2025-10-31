# file: voter_analytics/views.py
# author: Cody Headings, codyh@bu.edu, 10/30/2025
# desc: view functions to return html renders

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
from datetime import date
import plotly
import plotly.graph_objs as go

# Create your views here.
class VoterListView(ListView):
    '''View to display list of voter info'''
 
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        """Add variables to context data for view."""
        context = super().get_context_data(**kwargs)
        context["get_request"] = self.request.GET
        years = range(1910, 2011)
        context["years"] = years
        return context
    
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

class VoterGraphsView(ListView):
    """View to display graphs of voter data."""

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        """Method to add data to context of view."""
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        context = super().get_context_data(**kwargs)
        context["get_request"] = self.request.GET
        years = range(1910, 2011)
        context["years"] = years

        year_counts = {}
        for v in voters:
            year = v.dob.year
            if year in year_counts:
                year_counts[year] += 1
            else:
                year_counts[year] = 1

        years_sorted = sorted(year_counts.items())
        x_years = [year for year, _ in years_sorted]
        y_counts = [count for _, count in years_sorted]

        fig_dob = go.Bar(x=x_years, y=y_counts)
        graph_div_dob = plotly.offline.plot(
            {"data": [fig_dob],
             "layout_title_text": f"Voters by Year of Birth (n={voters.count()})"},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_dob'] = graph_div_dob

        party_counts = {}
        for v in voters:
            party = v.party
            if party in party_counts:
                party_counts[party] += 1
            else:
                party_counts[party] = 1

        fig_party = go.Pie(
            labels=list(party_counts.keys()),
            values=list(party_counts.values())
        )
        graph_div_party = plotly.offline.plot(
            {"data": [fig_party],
             "layout_title_text": f"Voters by Party Affiliation (n={voters.count()})"},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_party'] = graph_div_party

        elections = {
            "v20state": 0,
            "v21town": 0,
            "v21primary": 0,
            "v22general": 0,
            "v23town": 0,
        }

        for v in voters:
            if v.v20state == "TRUE":
                elections["v20state"] += 1
            if v.v21town == "TRUE":
                elections["v21town"] += 1
            if v.v21primary == "TRUE":
                elections["v21primary"] += 1
            if v.v22general == "TRUE":
                elections["v22general"] += 1
            if v.v23town == "TRUE":
                elections["v23town"] += 1

        fig_elect = go.Bar(
            x=list(elections.keys()),
            y=list(elections.values())
        )
        graph_div_elect = plotly.offline.plot(
            {"data": [fig_elect],
             "layout_title_text": f"Voter Participation in Elections (n={voters.count()})"},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_elect'] = graph_div_elect

        return context
    
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