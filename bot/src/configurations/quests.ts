import type Quest from "@models/Quest";

const quests: Array<Quest> = [
  {
    roleId: "1221444302270631946",
    taskType: "ggServerDied",
    taskRequiredValue: 90,
    reward: {
      coins: 10,
    },
  },
  {
    roleId: "1221444505740251216",
    taskType: "firstRule",
    taskRequiredValue: 60,
    reward: {
      coins: 8,
    },
  },
  {
    roleId: "1221445270345224233",
    taskType: "messages",
    taskRequiredValue: 1_000,
    reward: {
      coins: 15,
    },
  },
  {
    roleId: "1221445757824143402",
    taskType: "messageReactions",
    taskRequiredValue: 500,
    reward: {
      coins: 50,
    },
  },
  {
    roleId: "1221445352905773148",
    taskType: "messageReactions",
    taskRequiredValue: 50,
    reward: {
      coins: 10,
    },
  },
  {
    roleId: "1221445144050401390",
    taskType: "messages",
    taskRequiredValue: 100,
    reward: {
      coins: 25,
    },
  },
  {
    roleId: "1221881476300144650",
    taskType: "whenServer",
    taskRequiredValue: 30,
    reward: {
      coins: 5,
    },
  },
  {
    roleId: "1221444196661985331",
    taskType: "mediaOrMemes",
    taskRequiredValue: 30,
    reward: {
      coins: 5,
    },
  },
];

export default quests;
