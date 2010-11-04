#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
core.frontend
-------------
"""


from django.http import HttpResponse

from sites import site
from django.utils.translation import ugettext_lazy as _

from cyclope.utils import template_for_request

class FrontendView(object):
    """Parent class for frontend views.

    Class Attributes:

        name: name of the view (must be unique among registered views)

        verbose_name

        params(dict): keyword arguments that will be passed to get_response

        is_default(boolean): is this the default view for the model?

        is_instance_view(boolean): sets whether the view needs a content_object

        is_content_view(boolean): sets whether the view can be used for main page content

        is_region_view(boolean): sets whether the view can be included in layout regions
        
    """
    name = ''
    verbose_name = ''
    is_default = False
    is_instance_view = True
    is_content_view = False
    is_region_view = False
    extra_context = {}
    params = {}

    def __call__(self, request, inline=False, *args, **kwargs):
        if self.params:
            kwargs.update(self.params)

        if inline:
            extra_context={'host_template': 'cyclope/inline_view.html'}
        else:
            extra_context={'host_template': template_for_request(request)}

        if self.is_instance_view:
            if 'content_object' in kwargs:
                content_object = kwargs.pop('content_object')
            else:
                slug = kwargs['slug']
                content_object = self.model.objects.get(slug=slug)
            response = self.get_response(request, extra_context, content_object,
                                         *args, **kwargs)
        else:
            response = self.get_response(request, extra_context)
        
        # inline will be True if the view was called from a region templatetag
        if not inline:
            response = HttpResponse(response)
            
        return response

    def get_response(self, request, extra_context, content_object=None):
        """Must be overriden by inheriting class and return a the view content
        """
        raise NotImplementedError()

    def get_url_pattern(self, model):
        if self.is_default:
            return '%s/(?P<slug>[\w-]+)/$'\
                    % (model._meta.object_name.lower())

        if self.is_instance_view:
            return '%s/(?P<slug>[\w-]+)/View/%s'\
                    % (model._meta.object_name.lower(), self.name)
        else:
            return '%s/View/%s'\
                    % (model._meta.object_name.lower(), self.name)

##########
# autodiscover() is an almost exact copy of
# django.contrib.admin.autodiscover()

# A flag to tell us if autodiscover is running.  autodiscover will set this to
# True while running, and False when it finishes.
LOADING = False

def autodiscover():
    """Auto-discover frontend_views module for each INSTALLED_APP
    and fail silently when not present.

    This forces an import on them to register frontend views.
    """
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    from django.utils.importlib import import_module
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            app_path = mod.__path__
        except AttributeError:
            continue
        try:
            imp.find_module('frontend_views', app_path)
        except ImportError:
            continue
        import_module('%s.frontend_views' % app)

    for model in site._registry:
        default_view = [ view
                        for view in site._registry[model]
                        if view.is_default == True ]
        if len(default_view) == 0:
            raise(Exception(
                _(u'No default view has been set for %s' % model)))
        elif len(default_view) > 1:
            raise(Exception(
                _(u'You can set only one default view for %s' % model)))

    LOADING = False

################
