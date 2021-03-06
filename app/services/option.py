import importlib
import inspect

from hobbit_core.db import EnumExt


class OptionService:

    @classmethod
    def get_options(cls):
        return {
            name: obj.to_opts(verbose=True)
            for name, obj in importlib.import_module(
                'app.models.consts').__dict__.items()
            if inspect.isclass(obj) and issubclass(obj, EnumExt) and
            obj != EnumExt
        }
