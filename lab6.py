class GameCharacter:
    def __init__(self, health, stamina, damage):
        self.health = health
        self.stamina = stamina
        self.damage = damage

    def calculate_hits_until_exhaustion(self):
        # 计算耐力耗尽前的攻击次数
        print('Hellos')
        return self.stamina  # 假设每次攻击消耗1点耐力

    def __add__(self, other):
        # 附加任务：重载加法运算符
        if type(self) != type(other):
            raise TypeError("不能对不同类型进行加法操作")
        # 返回合并后的新对象
        return type(self)(
            self.health + other.health,
            self.stamina + other.stamina,
            self.damage + other.damage
        )


class WeakEnemy(GameCharacter):
    def __init__(self, health, stamina, damage, special_field):
        super().__init__(health, stamina, damage)
        self.special_field = special_field  # 独特字段

    def calculate_hits_to_defeat(self, attacker_damage):
        # 计算击败弱敌人所需的攻击次数
        return self.health // attacker_damage


class Boss(GameCharacter):
    def __init__(self, health, stamina, damage, boss_ability):
        super().__init__(health, stamina, damage)
        self.boss_ability = boss_ability  # 独特字段

    def calculate_hits_to_defeat(self, attacker_damage):
        # 计算击败BOSS所需的攻击次数，可能有特殊逻辑
        return self.health // attacker_damage * 2  # 例如BOSS有减伤


character = GameCharacter(10, 10, 20)
res = character.calculate_hits_until_exhaustion()
print(res)