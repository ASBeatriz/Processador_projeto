library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity reg1bit is
    port(
        clk, reset, entrada : in std_logic;
        q, qn : out std_logic
    );
end entity;

architecture behavior of reg1bit is

signal qsig, qnsig : std_logic;

begin
    process(clk, reset)
    begin
        if(reset = '0') then
            qsig <= '0';
            qnsig <= '1';
        elsif (rising_edge(clk)) then
            qsig <= entrada;
            qnsig <= not entrada;
        end if;

        q <= qsig;
        qn <= qnsig;

    end process;
end architecture;