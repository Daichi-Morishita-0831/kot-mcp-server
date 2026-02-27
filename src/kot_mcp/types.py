"""King of Time API のレスポンス型定義."""

from __future__ import annotations

from typing import TypedDict


class CompanyInfo(TypedDict, total=False):
    companyCode: str
    companyName: str


class Administrator(TypedDict, total=False):
    id: str
    code: str
    name: str
    email: str
    divisionCode: str
    divisionName: str


class Employee(TypedDict, total=False):
    key: str
    code: str
    lastName: str
    firstName: str
    lastNamePhonetics: str
    firstNamePhonetics: str
    divisionCode: str
    divisionName: str
    gender: str
    typeCode: str
    typeName: str
    employeeGroups: list[dict]


class Division(TypedDict, total=False):
    code: str
    name: str
    key: str


class DailyWorking(TypedDict, total=False):
    employeeKey: str
    date: str
    clockIn: str | None
    clockOut: str | None
    workingMinutes: int | None
    overtimeMinutes: int | None
    lateMinutes: int | None
    earlyLeaveMinutes: int | None


class MonthlyWorking(TypedDict, total=False):
    employeeKey: str
    workingDays: float | None
    workingMinutes: int | None
    overtimeMinutes: int | None
    lateCount: int | None
    earlyLeaveCount: int | None
    absentCount: int | None


class TimeRecord(TypedDict, total=False):
    employeeKey: str
    date: str
    time: str
    type: int  # 1:出勤, 2:退勤, 3:外出, 4:戻り


class ScheduleRequest(TypedDict, total=False):
    id: str
    employeeKey: str
    employeeName: str
    date: str
    requestType: str
    status: str
    note: str


class ApiError(TypedDict):
    code: str
    message: str
