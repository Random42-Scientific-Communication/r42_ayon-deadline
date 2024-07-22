# -*- coding: utf-8 -*-
"""Collector plugin for frames data on ROP instances."""
import hou  # noqa
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


class CollectR42HoudiniPublishAttributes(pyblish.api.InstancePlugin,
                                         AYONPyblishPluginMixin):
    """We condense all the UI information here
    In this case, we could share parameters
    """

    label = "Collect R42 Houdini Publish Attributes"
    order = pyblish.api.CollectorOrder + 0.499
    hosts = ["houdini"]
    families = ["usdrender",
                "redshift_rop",
                "arnold_rop",
                "mantra_rop",
                "karma_rop",
                "vray_rop"]
    targets = ["local"]
    settings_category = "deadline"

    export_group = ""
    group = ""
    export_priority = 50
    export_chunk_size = 10
    use_preview_frames = False
    preview_priority = 50
    preview_frame_skip = 2
    priority = 50
    chunk_size = 1
    suspend_publish = False


    @classmethod
    def apply_settings(cls, project_settings):
        settings = project_settings["deadline"]["publish"]["HoudiniSubmitDeadline"]  # noqa

        # Take some defaults from settings
        cls.export_group = settings.get("export_group",
                                        cls.export_group)
        cls.group = settings.get("group",
                                 cls.group)
        cls.priority = settings.get("priority",
                                    cls.priority)
        cls.export_priority = settings.get("export_priority",
                                           cls.export_priority)
        cls.chunk_size = settings.get("chunk_size",
                                      cls.chunk_size)
        cls.export_chunk_size = settings.get("export_chunk_size",
                                             cls.export_chunk_size)

    @classmethod
    def get_attribute_defs(cls):
        return [
            TextDef(
                "group",
                default=cls.group,
                label="Group Name"
            ),
            TextDef(
                "export_group",
                default=cls.export_group,
                label="Export Group Name"
            ),
            BoolDef(
                "use_preview_frames",
                default=cls.use_preview_frames,
                label="Use Preview Frames"
            ),
            NumberDef(
                "export_priority",
                label="Export Priority",
                default=cls.export_priority,
                decimals=0
            ),
            NumberDef(
                "export_chunk_size",
                label="Export Frames Per Task",
                default=cls.export_chunk_size,
                decimals=0,
                minimum=1,
                maximum=1000
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
            NumberDef(
                "priority",
                label="Priority",
                default=cls.priority,
                decimals=0
            ),
            NumberDef(
                "chunk_size",
                label="Frames Per Task",
                default=cls.chunk_size,
                decimals=0,
                minimum=1,
                maximum=1000
            ),
            BoolDef(
                "suspend_publish",
                default=cls.suspend_publish,
                label="Suspend publish"
            )
        ]


    def process(self, instance):
        attr_values = self.get_attr_values_from_data(instance.data)
        self.log.info(f"group : {attr_values.get('group', self.group)}")
        self.log.info(f"export_group : {attr_values.get('export_group', self.export_group)}")
        self.log.info(f"export_priority : {attr_values.get('export_priority', self.export_priority)}")
        self.log.info(f"export_chunk_size : {attr_values.get('export_chunk_size', self.export_chunk_size)}")
        self.log.info(f"use_preview_frames : {attr_values.get('use_preview_frames', self.use_preview_frames)}")
        self.log.info(f"preview_priority : {attr_values.get('preview_priority', self.preview_priority)}")
        self.log.info(f"preview_frame_skip : {attr_values.get('preview_frame_skip', self.preview_frame_skip)}")
        self.log.info(f"priority : {attr_values.get('priority', self.priority)}")
        self.log.info(f"chunk_size : {attr_values.get('chunk_size', self.chunk_size)}")
        self.log.info(f"suspend_publish : {attr_values.get('suspend_publish', self.suspend_publish)}")

        # Store all attributes
        instance.data["group"] = attr_values.get('group', self.group)
        instance.data["export_group"] = attr_values.get('export_group', self.export_group)
        instance.data["export_priority"] = attr_values.get('export_priority', self.export_priority)
        instance.data["export_chunk_size"] = attr_values.get('export_chunk_size', self.export_chunk_size)
        instance.data["use_preview_frames"] = attr_values.get('use_preview_frames', self.use_preview_frames)
        instance.data["preview_priority"] = attr_values.get('preview_priority', self.preview_priority)
        instance.data["preview_frame_skip"] = attr_values.get('preview_frame_skip', self.preview_frame_skip)
        instance.data["priority"] = attr_values.get('priority', self.priority)
        instance.data["chunk_size"] = attr_values.get('chunk_size', self.chunk_size)
        instance.data["suspend_publish"] = attr_values.get('suspend_publish', self.suspend_publish)

        # Store helper attributes
        instance.data["previewDeadlineSubmissionJob"] = None




