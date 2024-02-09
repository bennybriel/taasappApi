from django.utils.deprecation import MiddlewareMixin
from .signals import audit_trail_signal

import traceback


class AuditTrailMiddleware(MiddlewareMixin):
    def process_response(self, request, response):

        if response.status_code >= 200 and response.status_code < 300:
            # Get the view class from the resolver match info
            # view_class = request.resolver_match.func.cls

            view_class = None
            if hasattr(request.resolver_match.func, 'cls'):

                view_class = request.resolver_match.func.cls

            # Get the model from the view's queryset attribute
            # model = view_class.queryset.model.__name__
            model = None
            if hasattr(view_class, 'queryset'):
                model = view_class.queryset.model.__name__

            audit_trail_signal.send(
                sender=request.user.__class__,
                request=request,
                response=response,
                user=request.user,
                model=model,
                event_category=model,
                method=request.method,
                summary="{} {}".format(request.method, request.path),
            )
            return response
        else:
            # An error occurred, send the audit trail signal with an error message
            # Get the view class and model as described above
            view_class = None
            if hasattr(request.resolver_match.func, 'cls'):
                view_class = request.resolver_match.func.cls
            elif hasattr(request.resolver_match.func, 'view_class'):
                view_class = request.resolver_match.func.view_class

            model = None
            if view_class is not None and hasattr(view_class, 'queryset'):
                model = view_class.queryset.model.__name__

            # Build the error message from the traceback
            error_message = traceback.format_exc()

            audit_trail_signal.send(
                sender=request.user.__class__,
                request=request,
                response=response,
                user=request.user,
                model=model,
                event_category="Blog",
                method=request.method,
                summary="{} {} - ERROR".format(request.method, request.path),
                detail=error_message,
            )

        return response

    def process_exception(self, request, exception):
        # An exception occurred, send the audit trail signal with an error message
        # Get the view class and model as described above
        view_class = None
        if hasattr(request.resolver_match.func, 'cls'):
            view_class = request.resolver_match.func.cls
        elif hasattr(request.resolver_match.func, 'view_class'):
            view_class = request.resolver_match.func.view_class

        model = None
        if view_class is not None and hasattr(view_class, 'queryset'):
            model = view_class.queryset.model.__name__

        # Build the error message from the traceback
        error_message = traceback.format_exc()

        audit_trail_signal.send(
            sender=request.user.__class__,
            request=request,
            response=None,
            user=request.user,
            model=model,
            event_category="Blog",
            method=request.method,
            summary="{} {} - ERROR".format(request.method, request.path),
            detail=error_message,
        )
