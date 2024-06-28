import logging
import os
from pathlib import Path

from telethon import functions
from telethon.tl.types import InputMessagesFilterDocument, InputPeerChannel

from ..Config import Config
from ..helpers.utils import install_pip
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..utils import inst_done, load_module
from . import zedub

LOGS = logging.getLogger(__name__)
h_type = True

if Config.ZELZAL_A:

    async def install():
        if gvarstatus("PMLOG") and gvarstatus("PMLOG") != "false":
            delgvar("PMLOG")
        if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") != "false":
            delgvar("GRPLOG")
        try:
            entity = await zedub.get_input_entity(Config.ZELZAL_A)
            if isinstance(entity, InputPeerChannel):
                full_info = await zedub(
                    functions.channels.GetFullChannelRequest(channel=entity)
                )
            zilzal = full_info.full_chat.id
        except Exception:
            entity = await zedub.get_entity(Config.ZELZAL_A)
            full_info = await zedub(
                functions.channels.GetFullChannelRequest(channel=entity)
            )
            zilzal = full_info.full_chat.id
        documentss = await zedub.get_messages(
            zilzal, None, filter=InputMessagesFilterDocument
        )
        total = int(documentss.total)
        plgnm = 0
        for module in range(total):
            if plgnm == 22:
                break
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if plugin_name.endswith(".py"):
                if os.path.exists(f"zelz/plugins/{plugin_name}"):
                    return
                downloaded_file_name = await zedub.download_media(
                    await zedub.get_messages(Config.ZELZAL_A, ids=plugin_to_install),
                    "zelz/plugins/",
                )
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                flag = True
                check = 0
                while flag:
                    try:
                        load_module(shortname.replace(".py", ""))
                        plgnm += 1
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if check > 5:
                            break
        print(inst_done)
        addgvar("PMLOG", h_type)
        if gvarstatus("GRPLOOG") is not None:
            addgvar("GRPLOG", h_type)

    zedub.loop.create_task(install())
