from dataclasses import dataclass, asdict, field
import json
from typing import Type, TypeVar

T = TypeVar('T', bound='Config')

@dataclass
class Config:
    # TODO a class that can be saved to a json file (config.json)
    # are load with a cls method
    name: str
    version: str = field(default="0.1")
    openmp: int  = field(default=0)
    extra_compile_args: int = field(default=None)
    extra_link_args: int = field(default=None)
    include_dirs: list = field(default=None)

    def save(self, filename: str) -> None:
        """Save the configuration to a JSON file."""
        with open(filename, 'w') as file:
            json.dump(asdict(self), file, indent=4)

    @classmethod
    def load(cls: Type[T], filename: str) -> T:
        """Load the configuration from a JSON file."""
        with open(filename, 'r') as file:
            data = json.load(file)
        return cls(**data)