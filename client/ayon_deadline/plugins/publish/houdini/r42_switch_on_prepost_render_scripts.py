# -*- coding: utf-8 -*-
"""Helper script to turn on pre/post render scripts in scene."""
import hou  # noqa
import pyblish.api

class R42SwitchOnRenderScripts(pyblish.api.InstancePlugin):
    """We turn on all temporarily turned off pre/post render scripts
    """

    label = "R42 Switch On PrePost Render Scripts"
    order = pyblish.api.IntegratorOrder + 1
    hosts = ["houdini"]
    families = ["usdrender",
                "redshift_rop",
                "arnold_rop",
                "mantra_rop",
                "karma_rop",
                "vray_rop"]
    targets = ["local"]

    def process(self, instance):
        redshift_rop_prerender = "from nodes import redshift_rop_setup" \
                                 "\nredshift_rop_setup.pre_render_storyboard_image(hou.pwd())"
        redshift_rop_postrender = "from nodes import redshift_rop_setup" \
                                  "\nredshift_rop_setup.post_render_storyboard_image(hou.pwd())"

        for current_parm in instance.data["parms_to_turn_off_on"]:
            current_parm.set(1)

        for node in instance.data["node_to_clear_script"]:
            node.parm("prerender").set(redshift_rop_prerender)
            node.parm("postframe").set(redshift_rop_postrender)
