from typing import Any, Dict

import six
from connexion.apps.flask_app import FlaskJSONEncoder

from openapi_server.models.base_model_ import Model


class JSONEncoder(FlaskJSONEncoder):  # type: ignore
    include_nulls = False

    def default(self, o: Any) -> Dict[str, Any]:
        if not isinstance(o, Model):
            return FlaskJSONEncoder.default(self, o)  # type: ignore
        dikt = {}
        for attr, _ in six.iteritems(o.openapi_types):
            value = getattr(o, attr)
            if value is None and not self.include_nulls:
                continue
            attr = o.attribute_map[attr]
            dikt[attr] = value
        return dikt
