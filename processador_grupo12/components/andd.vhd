library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity andd is
    port(
        clock : in std_logic;
        first, second : in std_logic_vector(7 downto 0);
        result : out std_logic_vector(7 downto 0) 
    );
end entity;

architecture behavior of andd is
signal a, b, r : std_logic_vector(7 downto 0);


begin

a <= first;
b <= second;
    process(clock)
    begin
        if rising_edge(clock) then
            for i in 0 to 7 loop
                r(i) <= a(i) and b(i);
            end loop;
        end if;
    end process;

    result <= r;
end architecture;
