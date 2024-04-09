import type Quest from "@models/Quest";

const quests: Array<Quest> = [
  {
    roleId: "1221444302270631946",
    taskType: "ggServerDied",
    taskRequiredVal: 90,
    reward: {
      coins: 10,
    },
  },
  {
    roleId: "1221444505740251216",
    taskType: "firstRule",
    taskRequiredVal: 60,
    reward: {
      coins: 8,
    },
  },
  {
    roleId: "1221445270345224233",
    taskType: "messages",
    taskRequiredVal: 1_000,
    reward: {
      coins: 15,
    },
  },
  {
    roleId: "1221445757824143402",
    taskType: "messageReactions",
    taskRequiredVal: 500,
    reward: {
      coins: 50,
    },
  },
  {
    roleId: "1221445352905773148",
    taskType: "messageReactions",
    taskRequiredVal: 50,
    reward: {
      coins: 10,
    },
  },
  {
    roleId: "1221445144050401390",
    taskType: "messages",
    taskRequiredVal: 100,
    reward: {
      coins: 25,
    },
  },
  {
    roleId: "1221881476300144650",
    taskType: "whenServer",
    taskRequiredVal: 30,
    reward: {
      coins: 5,
    },
  },
  {
    roleId: "1221444196661985331",
    taskType: "mediaOrMemes",
    taskRequiredVal: 30,
    reward: {
      coins: 5,
    },
  },
];

export default quests;
