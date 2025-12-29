class GameCharacter:
    def __init__(self, health, stamina, damage):
        self.health = health
        self.stamina = stamina
        self.damage = damage

    def calculate_hits_until_exhaustion(self):
        # 计算耐力耗尽前的攻击次数（每次攻击消耗1点耐力）
        return self.stamina

    def __add__(self, other):
        # 重载加法运算符：合并两个相同类型的对象
        if type(self) != type(other):
            raise TypeError("不能对不同类型进行加法操作")
        return type(self)(
            self.health + other.health,
            self.stamina + other.stamina,
            self.damage + other.damage
        )

    def calculate_hits_to_defeat(self, attacker_damage):
        # 默认实现：计算击败此角色所需的攻击次数
        import math
        return math.ceil(self.health / attacker_damage)


class WeakEnemy(GameCharacter):
    def __init__(self, health, stamina, damage, special_field):
        super().__init__(health, stamina, damage)
        self.special_field = special_field  # 独特字段

    def calculate_hits_to_defeat(self, attacker_damage):
        # 弱敌人没有特殊防御，直接按血量除以伤害
        import math
        return math.ceil(self.health / attacker_damage)


class Boss(GameCharacter):
    def __init__(self, health, stamina, damage, boss_ability):
        super().__init__(health, stamina, damage)
        self.boss_ability = boss_ability  # 独特字段

    def calculate_hits_to_defeat(self, attacker_damage):
        # BOSS有减伤，例如：实际承受伤害为一半，所以需要两倍攻击次数
        import math
        return math.ceil(self.health / attacker_damage) * 2


# 示例使用
if __name__ == "__main__":
    character = GameCharacter(10, 10, 20)
    print("角色可攻击次数:", character.calculate_hits_until_exhaustion())  # 输出: 10

    weak_enemy = WeakEnemy(50, 8, 10, "weakness")
    boss = Boss(100, 15, 25, "regeneration")

    print("击败弱敌人所需攻击次数:", weak_enemy.calculate_hits_to_defeat(10))  # 5
    print("击败BOSS所需攻击次数:", boss.calculate_hits_to_defeat(10))         # 20

    # 测试加法运算符
    new_char = character + character
    print("合并后角色属性:", new_char.health, new_char.stamina, new_char.damage)

    # 尝试不同类相加会报错
    try:
        result = character + weak_enemy
    except TypeError as e:
        print("错误捕获:", e)
