from typing import Any
from custom_components.ecoflow_cloud.api import EcoflowApiClient
from custom_components.ecoflow_cloud.devices import const, BaseDevice
from custom_components.ecoflow_cloud.entities import BaseSensorEntity, BaseNumberEntity, BaseSwitchEntity, BaseSelectEntity
from custom_components.ecoflow_cloud.number import MaxBatteryLevelEntity, MinBatteryLevelEntity, MinGenStartLevelEntity, MaxGenStopLevelEntity
from custom_components.ecoflow_cloud.select import TimeoutDictSelectEntity
from custom_components.ecoflow_cloud.sensor import (
    LevelSensorEntity, WattsSensorEntity, RemainSensorEntity, TempSensorEntity,
    CapacitySensorEntity, QuotaStatusSensorEntity
)
from custom_components.ecoflow_cloud.switch import BeeperEntity, EnabledEntity

class DeltaPro3(BaseDevice):
    def sensors(self, client: EcoflowApiClient) -> list[BaseSensorEntity]:
        return [
            LevelSensorEntity(client, self, "bmsBattSoc", const.MAIN_BATTERY_LEVEL)
                .attr("bmsDesignCap", const.ATTR_DESIGN_CAPACITY, 0),
            CapacitySensorEntity(client, self, "bmsDesignCap", const.MAIN_DESIGN_CAPACITY, False),
            LevelSensorEntity(client, self, "cmsBattSoc", const.COMBINED_BATTERY_LEVEL),

            WattsSensorEntity(client, self, "powInSumW", const.TOTAL_IN_POWER),
            WattsSensorEntity(client, self, "powOutSumW", const.TOTAL_OUT_POWER),

            WattsSensorEntity(client, self, "powGetAcIn", const.AC_IN_POWER),
            WattsSensorEntity(client, self, "powGetAcHvOut", "AC Out HV Power"),
            WattsSensorEntity(client, self, "powGetAcLvOut", "AC Out LV Power"),

            WattsSensorEntity(client, self, "powGetPvH", "Solar HV In Power"),
            WattsSensorEntity(client, self, "powGetPvL", "Solar LV In Power"),

            WattsSensorEntity(client, self, "powGet12v", "12V DC Out Power"),
            WattsSensorEntity(client, self, "powGet24v", "24V DC Out Power"),

            WattsSensorEntity(client, self, "powGetQcusb1", const.USB_QC_1_OUT_POWER),
            WattsSensorEntity(client, self, "powGetQcusb2", const.USB_QC_2_OUT_POWER),
            WattsSensorEntity(client, self, "powGetTypec1", const.TYPEC_1_OUT_POWER),
            WattsSensorEntity(client, self, "powGetTypec2", const.TYPEC_2_OUT_POWER),

            RemainSensorEntity(client, self, "cmsChgRemTime", const.CHARGE_REMAINING_TIME),
            RemainSensorEntity(client, self, "cmsDsgRemTime", const.DISCHARGE_REMAINING_TIME),

            TempSensorEntity(client, self, "bmsMaxCellTemp", const.BATTERY_TEMP),
            TempSensorEntity(client, self, "bmsMinCellTemp", const.MIN_CELL_TEMP, False),

            QuotaStatusSensorEntity(client, self)
        ]

    def numbers(self, client: EcoflowApiClient) -> list[BaseNumberEntity]:
        return [
            MaxBatteryLevelEntity(client, self, "cmsMaxChgSoc", const.MAX_CHARGE_LEVEL, 50, 100,
                                  lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgMaxChgSoc": value}}),
            MinBatteryLevelEntity(client, self, "cmsMinDsgSoc", const.MIN_DISCHARGE_LEVEL, 0, 30,
                                  lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgMinDsgSoc": value}}),
            MinGenStartLevelEntity(client, self, "cmsOilOnSoc", const.GEN_AUTO_START_LEVEL, 0, 30,
                                   lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgCmsOilOnSoc": value}}),
            MaxGenStopLevelEntity(client, self, "cmsOilOffSoc", const.GEN_AUTO_STOP_LEVEL, 50, 100,
                                  lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgCmsOilOffSoc": value}}),
        ]

    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        return [
            BeeperEntity(client, self, "enBeep", const.BEEPER,
                         lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgBeepEn": value}}),
            EnabledEntity(client, self, "llcGFCIFlag", "GFCI",
                          lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgLlcGFCIFlag": value}}),
            EnabledEntity(client, self, "xboostEn", const.XBOOST_ENABLED,
                          lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgXboostEn": value}}),
            EnabledEntity(client, self, "flowInfoAcHvOut", "AC Out HV",
                          lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgHvAcOutOpen": value}}),
            EnabledEntity(client, self, "flowInfoAcLvOut", "AC Out LV",
                          lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgLvAcOutOpen": value}}),
            EnabledEntity(client, self, "flowInfo12v", "12V DC Out",
                          lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgDc12vOutOpen": value}}),
            EnabledEntity(client, self, "acEnergySavingOpen", "AC Energy Saving",
                          lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgAcEnergySavingOpen": value}}),
        ]

    def selects(self, client: EcoflowApiClient) -> list[BaseSelectEntity]:
        return [
            TimeoutDictSelectEntity(client, self, "acStandbyTime", const.AC_TIMEOUT, const.AC_TIMEOUT_OPTIONS,
                                    lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgAcStandbyTime": value}}),
            TimeoutDictSelectEntity(client, self, "dcStandbyTime", const.DC_TIMEOUT, const.DC_TIMEOUT_OPTIONS,
                                    lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgDcStandbyTime": value}}),
            TimeoutDictSelectEntity(client, self, "screenOffTime", const.SCREEN_TIMEOUT, const.SCREEN_TIMEOUT_OPTIONS,
                                    lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgScreenOffTime": value}}),
            TimeoutDictSelectEntity(client, self, "devStandbyTime", const.UNIT_TIMEOUT, const.UNIT_TIMEOUT_OPTIONS,
                                    lambda value: {"sn": self.device_info.sn, "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": True, "params": {"cfgDevStandbyTime": value}}),
        ]


    def _prepare_data(self, raw_data: bytes) -> dict[str, Any]:
        res = super()._prepare_data(raw_data)
        
        new_params = {}
        if "param" in res:
            new_params.update(res.pop("param"))
        if "params" in res:
            new_params.update(res.get("params", {}))

        mapping = {
            "cfgMaxChgSoc": "cmsMaxChgSoc",
            "cfgMinDsgSoc": "cmsMinDsgSoc",
            "cfgCmsOilOnSoc": "cmsOilOnSoc",
            "cfgCmsOilOffSoc": "cmsOilOffSoc",
            "cfgBeepEn": "enBeep",
            "cfgLlcGFCIFlag": "llcGFCIFlag",
            "cfgXboostEn": "xboostEn",
            "cfgHvAcOutOpen": "flowInfoAcHvOut",
            "cfgLvAcOutOpen": "flowInfoAcLvOut",
            "cfgDc12vOutOpen": "flowInfo12v",
            "cfgAcEnergySavingOpen": "acEnergySavingOpen",
            "cfgAcStandbyTime": "acStandbyTime",
            "cfgDcStandbyTime": "dcStandbyTime",
            "cfgScreenOffTime": "screenOffTime",
            "cfgDevStandbyTime": "devStandbyTime"
        }
        
        for cfg_k, cms_k in mapping.items():
            if cfg_k in new_params:
                new_params[cms_k] = new_params[cfg_k]

        res["params"] = new_params
        return res
