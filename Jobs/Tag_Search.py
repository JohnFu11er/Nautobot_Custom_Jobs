from nautobot.extras.jobs import *
from nautobot.dcim.models import Device, Interface
from nautobot.extras.models import Tag



class TagSearch(Job):

    target_tag = ObjectVar(
        description="Select the tag to search for",
        model=Tag
    )

    class Meta:
        name = "Search for tags assinged to an interface"
        description = "Tag filtering tool"
        commit_default = False
    
    def run(self, data, commit):
        interfaces = Interface.objects.filter(tags__name__startswith= data['target_tag'].name)
        if interfaces:
            for interface in interfaces:
                tag_names = "".join([str(i.name) for i in interface.tags.all() if data['target_tag'].name in i.name])
                self.log_success(
                    f"{interface.name} on device {interface.device.name} is tagged with: {tag_names}"
                )
        else:
            self.log_failure(f"No devices have interfaces with the '{data['target_tag']}' tag assigned.")
