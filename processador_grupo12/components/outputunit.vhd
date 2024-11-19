library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

--perguntar do clock para o aluno PAE, precisa de um clock e um enable?
entity outputunit is
    port(
        enable_display : in std_logic;
        receive : in std_logic_vector(7 downto 0);
        deliver : out std_logic_vector(7 downto 0)
    );
end entity;

architecture behavior of outputunit is

signal aux : std_logic_vector(7 downto 0);

begin
    process(enable_display)
    begin 
        if(enable_display = '1') then
            aux <= receive;
        end if;

        deliver <= aux;

    end process;
end architecture;