# -*- coding: utf-8 -*-
"""Collector plugin for frames data on ROP instances."""
import pyblish.api
from ayon_core.lib import (
    is_in_tests,
    BoolDef,
    NumberDef,
    EnumDef,
    TextDef
)
from ayon_core.pipeline import (
    AYONPyblishPluginMixin
)


class CollectR42JobInfo(pyblish.api.InstancePlugin,
                        AYONPyblishPluginMixin):
    """
    We collect preview renders attributes here
    """

    label = "R42 Collect Preview Attributes"
    hosts = ['max', 'houdini', 'blender']
    families = ["maxrender", "redshift_rop", "mantra_rop", "karma_rop"]
    targets = ["local"]
    order = pyblish.api.CollectorOrder + 0.419
    settings_category = "deadline"

    use_preview_frames = False
    preview_priority = 50
    preview_frame_skip = 2
    preview_initial_status = "Active"

    @classmethod
    def get_attribute_defs(cls):
        defs = super(CollectR42JobInfo, cls).get_attribute_defs()
        defs.extend([
            BoolDef(
                "use_preview_frames",
                default=cls.use_preview_frames,
                label="Use Preview Frames"
            ),
            NumberDef(
                "preview_priority",
                label="Preview Priority",
                default=cls.preview_priority,
                decimals=0
            ),
            NumberDef(
                "preview_frame_skip",
                label="Preview Frame Skip",
                default=cls.preview_frame_skip,
                decimals=0
            ),
            EnumDef("preview_initial_status",
                    label="Preview Render Initial Status",
                    items=["Active", "Suspended"],
                    default=cls.preview_initial_status),
        ])
        return defs


    def process(self, instance):
        attr_values = self.get_attr_values_from_data(instance.data)
        self.log.info(f"use_preview_frames : {attr_values.get('use_preview_frames', self.use_preview_frames)}")
        self.log.info(f"preview_priority : {attr_values.get('preview_priority', self.preview_priority)}")
        self.log.info(f"preview_frame_skip : {attr_values.get('preview_frame_skip', self.preview_frame_skip)}")
        self.log.info(f"preview_initial_status : {attr_values.get('preview_initial_status', self.preview_initial_status)}")

        # Store all attributes
        instance.data["use_preview_frames"] = attr_values.get('use_preview_frames', self.use_preview_frames)
        instance.data["preview_priority"] = attr_values.get('preview_priority', self.preview_priority)
        instance.data["preview_frame_skip"] = attr_values.get('preview_frame_skip', self.preview_frame_skip)
        instance.data["preview_initial_status"] = attr_values.get('preview_initial_status', self.preview_initial_status)

        # Store helper attributes
        instance.data["previewDeadlineSubmissionJob"] = None

