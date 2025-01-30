# -*- coding: utf-8 -*-
"""Helper script to turn off pre/post render scripts in scene."""
import hou  # noqa
import pyblish.api
from contextlib import suppress

from ayon_core.pipeline import (
    AYONPyblishPluginMixin
)

class R42SwitchOffRenderScripts(pyblish.api.InstancePlugin,
                                AYONPyblishPluginMixin):
    """We find all nodes in the scene and turn
    off pre/post render scripts temporarily before submitting
    to the farm
    """

    label = "r42 Switch Off PrePost Render Scripts"
    order = pyblish.api.ExtractorOrder - 0.5
    hosts = ["houdini"]
    families = ["usdrender",
                "redshift_rop",
                "arnold_rop",
                "mantra_rop",
                "karma_rop",
                "vray_rop"]
    targets = ["local"]
    settings_category = "deadline"

    node_type_list_to_check = ["Redshift_ROP", "filecache::2.0"]

    def process(self, instance):


        parent = hou.node("/obj/")
        all_nodes = list(parent.allSubChildren())
        parent = hou.node("/out/")
        out_nodes = list(parent.allSubChildren())
        all_nodes.extend(out_nodes)

        parms_to_turn_off_on = []
        node_to_clear_script = []

        for node in all_nodes:
            if node.type().name() in self.node_type_list_to_check:
                if node.parm("tprerender").eval() and node.parm("prerender").eval():
                    parms_to_turn_off_on.append(node.parm("tprerender"))
                if node.parm("tpreframe").eval() and node.parm("preframe").eval():
                    parms_to_turn_off_on.append(node.parm("tpreframe"))
                if node.parm("tpostframe").eval() and node.parm("postframe").eval():
                    parms_to_turn_off_on.append(node.parm("tpostframe"))
                if node.parm("tpostrender").eval() and node.parm("postrender").eval():
                    parms_to_turn_off_on.append(node.parm("tpostrender"))
                with suppress(AttributeError):
                    if node.parm("tpostwrite").eval() and node.parm("postwrite").eval():
                        parms_to_turn_off_on.append(node.parm("tpostwrite"))

                if node.type().name() == "Redshift_ROP":
                    node_to_clear_script.append(node)

        for current_parm in parms_to_turn_off_on:
            current_parm.set(0)

        for node in node_to_clear_script:
            node.parm("prerender").set("")
            node.parm("postframe").set("")


        # Store data so we can turn it back on later
        instance.data["parms_to_turn_off_on"] = parms_to_turn_off_on
        instance.data["node_to_clear_script"] = node_to_clear_script
